/* Header file for BST implementation */
#define MAXLEN      128
#define ROWLEN      516
#define BUFFER      1
#define FOUND       1
#define NOT_FOUND   0

/* Struct Prototypes */
typedef struct node node_t;

struct node {
    void    *data;
    node_t  *left;
    node_t  *right;
    node_t  *next;
};

typedef struct {
    node_t *root;
    int (*cmp)(void*,void*);
} btree_t;

typedef struct {
    char    name[MAXLEN];
    char    id[MAXLEN];
    char    sex[MAXLEN];
    char    age[MAXLEN];
    char    height[MAXLEN];
    char    weight[MAXLEN];
    char    team[MAXLEN];
    char    NOC[MAXLEN];
    char    games[MAXLEN];
    char    year[MAXLEN];
    char    season[MAXLEN];
    char    city[MAXLEN];
    char    sport[MAXLEN];
    char    event[MAXLEN];
    char    medal[MAXLEN];
} record_t;

/* Function Prototypes */
btree_t *create_bst(int func(void*,void*));
void search(btree_t *tree, void *value, FILE *data_out);
btree_t *insert(btree_t *tree, void *value);
void free_tree(btree_t *tree);
static void *search_tree_recursively(node_t *root, void *key, int cmp(void*,void*), int *no_comparisions, FILE *data_out);
static node_t *insert_recursively(node_t *root, node_t *new, int cmp(void*,void*));
static void recursive_free_tree(node_t *root);
int cmp(void *name1, void *name2);