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

/* Main Function */
int 
main(int argc, char const *argv[]) {
    /* Temp CSV line array */
    char csv_line[ROW_LEN];

    /* Search Name */
    char name[ROW_LEN];

    /* BST init */
    btree_t *tree;
    tree = create_bst(cmp);
    assert(tree!=NULL);

    /* File init */
    FILE *data_in;
    FILE *data_out;

    data_in = fopen(argv[1], "r");
    if (data_in == NULL) {
        free(tree);
        exit(-1);
    }
    data_out = fopen(argv[2], "w+");

    /* Read lines in */
    while(fgets(csv_line, sizeof(csv_line), data_in)) {
        read_csv(csv_line, tree);
    }

    
    while (fgets(name, sizeof(name), stdin) != NULL) {
        /* Hey it's my who had the issue using \r or \n from Piazza. Let
           me know if this is right. I used a new keyfile that was created using
           UNIX formatting instead of a normal text file. It seems to work for
           both windows and UNIX now. A lot of other students seemed to have
           this issue so please take it into consideration next time when you 
           give us sample inputs (at least a few rows not just one) */
        name[strcspn(name, "\n")] = '\0';

        if (!strlen(name)) {
            break;
        }
        
        search(tree, name, data_out);
    }

    /* Finish up */
    fclose(data_in);
    fclose(data_out);
    free_tree(tree);

    return 0;
}

/* Read in CSV using strtok */
void
read_csv(char *csv_line, btree_t *tree) {
    char *tokens;
    record_t *record;
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
    /* I poured my blood to fix double quotes and now its irrelevant :/ */
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
        fprintf(data_out, "Sex: %s ", p->sex);
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