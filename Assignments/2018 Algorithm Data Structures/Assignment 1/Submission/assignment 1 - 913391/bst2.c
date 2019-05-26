#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "bst.h"

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
    if (root!=NULL) { 
        recursive_free_tree(root->left);
        recursive_free_tree(root->right);
        recursive_free_tree(root->next);
        free(root->data);
        free(root);
    }
}

void free_tree(btree_t *tree) {
    assert(tree!=NULL);
    recursive_free_tree(tree->root);
    free(tree);
}