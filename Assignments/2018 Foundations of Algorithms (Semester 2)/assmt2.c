/* 
 * NER Text Analysis
 * COMP10002 Assignment 2
 * Written by Akira Wang, May 2018 (Student ID 913391)
 * Algorithms are fun 
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#define WORD_LEN        30  /* maximum length of any word; */
#define HASH_KEY        1   /* length of the '#' char */
#define PROBABILITIES   3   /* number of probabilities for the NER */
#define DICT_LEN        100 /* number of max unique names in the dict */
#define BUFFER          1   /* buffer for "%%%%%%%%%%" or '\0' */
#define PERCENTAGE      '%' /* percentage char */
#define WHITESPACE      ' ' /* whitespace char */
#define STAGE_4         4   /* Stage 4 */
#define STAGE_5         5   /* Stage 5 */
#define CERTAIN         100 /* Certain probability */

/* Definitions */
typedef char word_t[WORD_LEN+BUFFER];
typedef struct node node_t;

typedef struct {
    char    name[WORD_LEN+HASH_KEY+BUFFER];
    int     prob_first_name;
    int     prob_last_name;
    int     prob_non_name;
} name_dict_t;

struct node {
	word_t  word;
	node_t *next;
};

typedef struct {
	node_t *head;
	node_t *foot;
} list_t;

/* Function prototypes */
void init(name_dict_t dict[]);
void read_name(name_dict_t dict[], int index);
void read_prob(name_dict_t dict[], int index);
list_t *add_foot(list_t *sentence, word_t word);
void print_stage_1(name_dict_t dict[]);
void print_stage_2(name_dict_t dict[], int index);
void print_stage_3(list_t *node_list, word_t word);
void print_stage_4(name_dict_t dict[], list_t *sentence, int index);
void print_stage_5(name_dict_t dict[], list_t *sentence, int index);
int compare(const void *v1, const void *v2);
void find_word(name_dict_t dict[], const char *name, int index, int stage);
void find_index(name_dict_t keyword, name_dict_t dict[], int index, int stage);
void whitespace_aligner(int whitespace_count);
void label_word(name_dict_t dict[], int ner_index);
void name_entity_recognition(name_dict_t dict[], int ner_index);
/******************************************************************************
The functions below are written by Alistair Moffat, as an example for the book
"Programming, Problem Solving, and Abstraction with C", Pearson
Custom Books, Sydney, Australia, 2002; revised edition 2012,
ISBN 9781486010974.
******************************************************************************/
int getword(char W[], int limit);
list_t *make_empty_list(void);
void free_list(list_t *sentence);
/* Function(s) used may have been modified to be implemented in this assignment
*******************************************************************************
******************************************************************************/
int 
main(int argc, char *argv[]) {
    int index = 0;
    /* allocate array for name_dict_t * 101 elements */
    name_dict_t dict[sizeof(name_dict_t)*(DICT_LEN+BUFFER)];
    word_t word;
    list_t *sentence;

    init(dict);
    sentence = make_empty_list();
    assert(sentence!=NULL);
/******************************************************************************
|                            Stages 1 and 2                                   |
******************************************************************************/
    while (1) {
        read_name(dict, index);
        /* if the input is "%%%%%%%%%%" then break */
        if (dict[index].name[0] == PERCENTAGE) {
            dict[index].name[1] = '\0';
            break;
        }
        read_prob(dict, index);
        index++;
    }
/******************************************************************************
|                                Stage 3                                      |
******************************************************************************/
    /* garbage collect the '\n' character */
    getchar();
    while(getword(word, WORD_LEN+BUFFER) != EOF) {
        add_foot(sentence, word);
    }
/******************************************************************************
|                            Stages 4 and 5                                   |
******************************************************************************/
    print_stage_1(dict);
    print_stage_2(dict, index);
    print_stage_3(sentence, word);
    print_stage_4(dict, sentence, index);
    print_stage_5(dict, sentence, index);

    free_list(sentence);
    sentence = NULL;

    return 0;
    /* Done with this assignment rest in peace life */
}
/******************************************************************************
******************************************************************************/

/* Sets all the probabilities to 0's */
void init(name_dict_t dict[]) {
    int i;
    for (i = 0; i < DICT_LEN+HASH_KEY+BUFFER; i++) {
        dict[i].prob_first_name = 0;
        dict[i].prob_last_name = 0;
        dict[i].prob_non_name = 0;
    }
}

/* Reads a name input */
void read_name(name_dict_t dict[], int index) {
    scanf("%s", dict[index].name);
}

/* Reads a probability input */
void read_prob(name_dict_t dict[], int index) {
    scanf("%d", &dict[index].prob_first_name);
    scanf("%d", &dict[index].prob_last_name);
    scanf("%d", &dict[index].prob_non_name);
    /* garbage dispose the \n for the next dictionary entry */
    getchar();
}

/* Sets the node list to be empty */
list_t
*make_empty_list(void) {
    list_t *list;
	list = (list_t *)malloc(sizeof(*list));
    assert(list!=NULL);
    list->head = list->foot = NULL;
    return list;
}

/* Adds a new foot into the linked list */
list_t *add_foot(list_t *sentence, word_t word) {
    node_t *new;
    new = (node_t*)malloc(sizeof(*new));
    assert(sentence!=NULL && new!=NULL);
    strcpy(new->word, word);
    new->next = NULL;
    if (sentence->foot == NULL) {
        sentence->head = sentence->foot = new;
    }
    else {
        sentence->foot->next = new;
        sentence->foot = new;
    }
    return sentence;
}

/* Frees the node list */
void
free_list(list_t *sentence) {
    node_t *current, *prev;
    assert(sentence!=NULL);
    current = sentence->head;
    while (current) {
        prev = current;
        current = current->next;
        free(prev);
    }
    free(sentence);
}

/* Gets a word */
int
getword(char W[], int limit) {
    int c, len=0;
    while ((c=getchar())!=EOF && c== WHITESPACE) {
        /* do nothing */
    }
    if (c==EOF || c=='\n' || c=='\r') {
        return EOF;
    }
    W[len++] = c;
    while (len<limit && (c=getchar())!=EOF && isalpha(c)) {
        W[len++] = c;
    }
    W[len] = '\0';
    return 0;
}

/* Prints stage 1 */
void print_stage_1(name_dict_t dict[]) {
    printf("=========================Stage 1=========================\n");
    printf("Name 0: %s\n", dict[0].name+HASH_KEY);
    printf("Label probabilities: ");
    printf("%d%% ", dict[0].prob_first_name);
    printf("%d%% ", dict[0].prob_last_name);
    printf("%d%%\n", dict[0].prob_non_name);
    printf("\n");
}

/* Prints stage 2 */
void print_stage_2(name_dict_t dict[], int index) {
    float average = 0.0, counter = 0.0;
    int i, sum = 0;
    /* calculate the average number of characters */
    for (i = 0; i < index; i++) {
        sum += strlen(dict[i].name) - HASH_KEY;
        counter++;
    }
    average = sum / counter;
    if (index == 0) {
        average = 0.00;
    }
    printf("=========================Stage 2=========================\n");
    printf("Number of names: %d\n", index);
    printf("Average number of characters per name: %.2f\n", average);
    printf("\n");
}

/* Prints stage 3 */
void print_stage_3(list_t *sentence, word_t word) {
    node_t *current = sentence->head;
    printf("=========================Stage 3=========================\n");
    while (current) {
        printf("%s\n", current->word);
        current = current->next;
    }
    printf("\n");
}

/* Prints stage 4 */
void print_stage_4(name_dict_t dict[], list_t *sentence, int index) {
    node_t *current = sentence->head;
    int whitespace_count = 0;
    int stage = STAGE_4;
    printf("=========================Stage 4=========================\n");
    while (current) {
        printf("%s", current->word);
        /* calculate the number of whitespaces needed to align columns */
        whitespace_count = (WORD_LEN+HASH_KEY+BUFFER) - strlen(current->word);
        whitespace_aligner(whitespace_count);
        find_word(dict, current->word, index, stage);
        current = current->next;
    }
    printf("\n");
}

/* Compares 2 strings */
int compare(const void *v1, const void *v2) {
    const name_dict_t *c1 = v1;
    const name_dict_t *c2 = v2;
    return strcmp(c1->name, c2->name);
}

/* Finds a word in the dictionary using bsearch() */
void find_word(name_dict_t dict[], const char *name, int index, int stage) {
    /* assign a temp keyword for searching */
    name_dict_t keyword;
    strcpy(keyword.name, name);
    /* binary search for value */
    if (bsearch(keyword.name, dict->name+HASH_KEY, index, sizeof(*dict), compare)) {
        find_index(keyword, dict, index, stage);
    }
    else {
        printf("NOT_NAME\n");
    }
}

/* Finds the index of the word in the dictionary */
void find_index(name_dict_t keyword, name_dict_t dict[], int index, int stage) {
    int i = 0;
    int ner_index = 0;
    for (i = 0; i < index; i++) {
        /* check if strings match */
        if (strcmp(dict[i].name+HASH_KEY, keyword.name) == 0) {
            ner_index = i;
            /* Stage 4 label words */
            if (stage == STAGE_4) {
                label_word(dict, ner_index);
            }
            /* Stage 5 label words using probabilities */
            if (stage == STAGE_5) {
                name_entity_recognition(dict, ner_index);
            }
            break;
        }
    }
}

/* Stage 4 labelling for first_name or last_name */
void label_word(name_dict_t dict[], int ner_index) {
    int first_name = dict[ner_index].prob_first_name;
    int last_name = dict[ner_index].prob_last_name;
    if (first_name > 0 && last_name > 0) {
        printf("FIRST_NAME, LAST_NAME\n");
    }
    else if (first_name > 0) {
        printf("FIRST_NAME\n");
    }
    else if (last_name > 0) {
        printf("LAST_NAME\n");
    }
}

/* Prints whitespaces to align columns */
void whitespace_aligner(int whitespace_count) {
    while (whitespace_count > 0) {
        printf(" ");
        whitespace_count--;
    }
}

/* Prints stage 5 */
void print_stage_5(name_dict_t dict[], list_t *sentence, int index) {
    node_t *current = sentence->head;
    int whitespace_count = 0;
    int stage = STAGE_5;
    printf("=========================Stage 5=========================\n");
    while (current) {
        printf("%s", current->word);
        /* calculate the number of whitespaces needed to align columns */
        whitespace_count = (WORD_LEN+HASH_KEY+BUFFER) - strlen(current->word);
        whitespace_aligner(whitespace_count);
        find_word(dict, current->word, index, stage);
        current = current->next;
    }
}

/* Stage 5 Name Entity Recognition */
void name_entity_recognition(name_dict_t dict[], int ner_index) {
    int first_name = dict[ner_index].prob_first_name;
    int last_name = dict[ner_index].prob_last_name;
    int non_name = dict[ner_index].prob_non_name;
    int name_count = 0;
    /* SUM( Pr(is a name) ) < Pr(Non_Name) */
    if ( (first_name + last_name) < non_name) {
        printf("NOT_NAME\n");
    }
    /* Pr(First_Name) = 1 */
    else if (first_name == CERTAIN) {
        printf("FIRST_NAME\n");
        name_count++;
    }
    /* Pr(Last_Name) = 1 */
    else if (last_name == CERTAIN) {
        printf("LAST_NAME\n");
        name_count++;
    }
    else {
        /* Pr(First_Name | previous is last name) */
        if ( (first_name > last_name) && (name_count % 2 == 0 ) ) {
            printf("FIRST_NAME\n");
            name_count++;
        }
        /* Pr(Last_Name | previous is first name) */
        else if ( (last_name > first_name) && (name_count % 2 == 1) ) {
            printf("LAST_NAME\n");
            name_count++;
        }
        /* Pr(First_Name | previous is last name) */
        else if ( (last_name > first_name) && (name_count % 2 == 0 ) ) {
            printf("FIRST_NAME\n");
            name_count++;
        }
        /* Pr(Last_Name | previous is first name) */
        else if ( (first_name > last_name) && (name_count % 2 == 1) ) {
            printf("LAST_NAME\n");
            name_count++;
        }
        /* Pr(First_Name) = Pr(Last_Name) */
        else if ( (first_name == last_name) ) {
            /* Pr(First_Name | previous is a last name) */
            if (name_count % 2 == 0) {
                printf("FIRST_NAME\n");
                name_count++;
            }
            /* Pr(Last_Name | previous is first name) */
            else {
                printf("LAST_NAME\n");
                name_count++;
            }
        }
        else {
            /* All other random cases */
            printf("NOT_NAME\n");
       }
    }
}