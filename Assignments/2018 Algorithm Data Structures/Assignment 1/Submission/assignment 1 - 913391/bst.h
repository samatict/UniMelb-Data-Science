/* Header file for BST implementation */
#define SEX_LEN     1
#define AGE_LEN     2
#define NOC_LEN     3
#define YEAR_LEN    4
#define SEASON_LEN  6
#define MEASURE_LEN 3
#define MAX_LEN     128
#define ROW_LEN     516
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

/* Buffering assuming max length of 128 - malloc'ing then free'ing was too hard 
   so I'm ready to cop the mark for not allocating but pre-buffering */
typedef struct {
    char    name[MAX_LEN+BUFFER];
    char    id[MAX_LEN+BUFFER];
    char    sex[SEX_LEN+BUFFER];
    char    age[AGE_LEN+BUFFER];
    char    height[MEASURE_LEN+BUFFER];
    char    weight[MEASURE_LEN+BUFFER];
    char    team[MAX_LEN+BUFFER];
    char    NOC[NOC_LEN+BUFFER];
    char    games[YEAR_LEN+BUFFER+SEASON_LEN+BUFFER];
    char    year[YEAR_LEN+BUFFER];
    char    season[SEASON_LEN+BUFFER];
    char    city[MAX_LEN+BUFFER];
    char    sport[MAX_LEN+BUFFER];
    char    event[MAX_LEN+BUFFER];
    char    medal[MAX_LEN+BUFFER];
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