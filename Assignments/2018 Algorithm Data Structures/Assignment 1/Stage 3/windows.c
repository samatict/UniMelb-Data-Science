/******************************************************************************\
 * Name: Akira Wang                                                           *
 * Student ID: 913391                                                         *
 * Algorithms and Data Structures Assignment 1                                *
 * Date: 08/2018                                                              *
 * Algorithms are fun!                                                        *
\******************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "bst.h"

/* Function Prototypes */
void read_csv(char *csv_line, btree_t *tree);
void write_to_file(node_t *root, int result, FILE *data_out, void *key);


/* Create empty BST */
btree_t
*create_bst(int func(void*,void*)) {
    btree_t *tree;

    tree = malloc(sizeof(*tree));   
    assert(tree!=NULL);

    tree->root = NULL;
    tree->cmp = func;

    return tree;
}

/* Search Function */
static void
*search_tree_recursively(node_t *root, void *key, int cmp(void*,void*), int *no_comparisions, FILE *data_out) {
    int cmp_result;

    /* No matches */
    if (root == NULL) {
        write_to_file(root, NOT_FOUND, data_out, key);
        return NULL;
    }
    cmp_result = cmp(key, root->data);

    if (cmp_result < 0) {
        *no_comparisions += 1;
        return search_tree_recursively(root->left, key, cmp, no_comparisions, data_out);
    }
    else if (cmp_result > 0) {
        *no_comparisions += 1;
        return search_tree_recursively(root->right, key, cmp, no_comparisions, data_out);
    }
    else if (cmp_result == 0) {
        /* Found a result(s) */
        write_to_file(root, FOUND, data_out, key);
        if (!root->next) {
            /* Final comparision of the linked list so add 1 */
            *no_comparisions += 1;
            return NULL;
        }
        return search_tree_recursively(root->next, key, cmp, no_comparisions, data_out);
    }
    return NULL;
}

void
search(btree_t *tree, void *key, FILE *data_out) {
    int no_comparisions = 0;
    assert(tree!=NULL);
    search_tree_recursively(tree->root, key, tree->cmp, &no_comparisions, data_out);
    printf("%s --> %d\n",(char*)key, no_comparisions);
}

/* Insert Function */
static node_t
*insert_recursively(node_t *root, node_t *new, int cmp(void*,void*)) {
    if (root == NULL) {
        return new;
    }
    else {
        int cmp_result = cmp(new->data, root->data);

        if (cmp_result < 0) {
            root->left = insert_recursively(root->left, new, cmp);
        }
        else if (cmp_result > 0) {
            root->right = insert_recursively(root->right, new, cmp);
        }
        else {
            root->next = insert_recursively(root->next, new, cmp);
        }
    }
    return root;
}

btree_t
*insert(btree_t *tree, void *value) {
    node_t *new;
    
    new = malloc(sizeof(*new));
    assert(new!=NULL);
    assert(tree!=NULL);

    new->data = value;
    new->left = new->right = new->next = NULL;

    tree->root = insert_recursively(tree->root, new, tree->cmp);
    return tree;
}

/* Compare Function */
int
cmp(void *name1, void *name2) {
    record_t *p1=name1, *p2=name2;
    return strcmp(p1->name, p2->name);
}

/* Free BST Function */
static void
recursive_free_tree(node_t *root) {
    if (root) { 
        recursive_free_tree(root->left);
        recursive_free_tree(root->right);
        free(root);
    }
}

void free_tree(btree_t *tree) {
    assert(tree!=NULL);
    recursive_free_tree(tree->root);
    free(tree);
}

/* Main Function */
int 
main(int argc, char const *argv[]) {
    /* Temp CSV line array */
    char csv_line[ROWLEN];

    /* Search Name */
    char name[ROWLEN];

    /* BST init */
    btree_t *tree;
    tree = create_bst(cmp);
    assert(tree!=NULL);

    /* File init */
    FILE *data_in;
    FILE *data_out;
    data_in = fopen(argv[1], "r");
    data_out = fopen(argv[2], "a+");

    /* Read lines in */
    while(fgets(csv_line, sizeof(csv_line), data_in)) {
        read_csv(csv_line, tree);
    }

    while (fgets(name, sizeof(name), stdin) != NULL) {
        /* For Windows, I had to use \n but on the UNIX server only \r works */
        name[strcspn(name, "\n")] = '\0';

        /* If there is no stdin or input */
        if (!strlen(name)) {
            break;
        } 

        search(tree, name, data_out);
    }

    /* Finish up */
    fclose(data_in);
    fclose(data_out);
    free(tree);

    return 0;
}

/* Read in CSV using strtok , inspired by pd.read_csv(). 
   Full serious tho this was painful implementing so I ended up correcting it to
   fit - forgive me :(  
       
   NEVERMIND Nir bloody cucked us like Yasmeen. Here's the new function using strtok
*/
void
read_csv(char *csv_line, btree_t *tree) {
    char *tokens;
    record_t *record;
    /* malloc the actual record.value */
    record = (record_t*)malloc(sizeof(*record));

    tokens = strtok(csv_line, ",");
    strcpy(record->id, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->name, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->sex, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->age, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->height, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->weight, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->team, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->NOC, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->games, tokens);    
    tokens = strtok(NULL, ",");
    strcpy(record->year, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->season, tokens);
    tokens = strtok(NULL, ",");
    strcpy(record->city, tokens);
    tokens = strtok(NULL, ","); 
    strcpy(record->sport, tokens);
    tokens = strtok(NULL, ",");
    /* I poured my blood to fix this and now its irrelevant :/ */
    strcpy(record->event, tokens);
    tokens = strtok(NULL, "\n"); 
    tokens[strcspn(tokens, "\n")] = '\0';
    strcpy(record->medal, tokens);
    
    /* Free tokens */
    tokens = NULL;
    free(tokens);

    /* Insert struct into tree */
    insert(tree, record);
}

/* Write results into output file */
void
write_to_file(node_t *root, int result, FILE *data_out, void *key) {
    /* If FOUND */
    if (result) {
        record_t *p = root->data;
        fprintf(data_out, "%s --> ", p->name);
        fprintf(data_out, "ID: %s ", p->id);
        fprintf(data_out, "|| Sex: %s ", p->sex);
        fprintf(data_out, "|| Age: %s ", p->age);
        fprintf(data_out, "|| Height: %s ", p->height);
        fprintf(data_out, "|| Weight: %s ", p->weight);
        fprintf(data_out, "|| Team: %s ", p->team);
        fprintf(data_out, "|| NOC: %s ", p->NOC);
        fprintf(data_out, "|| Games: %s ", p->games);
        fprintf(data_out, "|| Year: %s ", p->year);
        fprintf(data_out, "|| Season: %s ", p->season);
        fprintf(data_out, "|| City: %s ", p->city);
        fprintf(data_out, "|| Sport: %s ", p->sport);
        fprintf(data_out, "|| Event: %s ", p->event);
        fprintf(data_out, "|| Medal: %s ||\n", p->medal);
    }
    /* If NOT FOUND */
    else {
        fprintf(data_out, "%s --> NOTFOUND\n", (char*)key);
    }
}

