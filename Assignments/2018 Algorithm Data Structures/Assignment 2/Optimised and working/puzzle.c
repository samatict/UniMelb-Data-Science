#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/types.h>
#include <sys/resource.h>
#include <sys/time.h>

#define TILE_LEN	16
#define ROW_LEN		4
#define COL_LEN		4
#define MOVES		4
#define TILE		1
#define BLANK_TILE	0

typedef struct node{
	int state[16];
	int g;
	int f;
	int prev_move;
} node;

/**
 * Global Variables
 */

// used to track the position of the blank in a state,
// so it doesn't have to be searched every time we check if an operator is applicable
// When we apply an operator, blank_pos is updated
int blank_pos;

// Initial node of the problem
node initial_node;

// Statistics about the number of generated and expendad nodes
unsigned long generated;
unsigned long expanded;


/**
 * The id of the four available actions for moving the blank (empty slot). e.x.
 * Left: moves the blank to the left, etc. 
 */

#define LEFT 0
#define RIGHT 1
#define UP 2
#define DOWN 3

/*
 * Helper arrays for the applicable function
 * applicability of operators: 0 = left, 1 = right, 2 = up, 3 = down 
 */
int ap_opLeft[]  = { 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1 };
int ap_opRight[]  = { 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0 };
int ap_opUp[]  = { 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
int ap_opDown[]  = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 };
int *ap_ops[] = { ap_opLeft, ap_opRight, ap_opUp, ap_opDown };


/* print state */
void print_state( int* s )
{
	int i;
	
	for( i = 0; i < 16; i++ )
		printf( "%2d%c", s[i], ((i+1) % 4 == 0 ? '\n' : ' ') );
}
      
void printf_comma (long unsigned int n) {
    if (n < 0) {
        printf ("-");
        printf_comma (-n);
        return;
    }
    if (n < 1000) {
        printf ("%lu", n);
        return;
    }
    printf_comma (n/1000);
    printf (",%03lu", n%1000);
}

/* copy the initial state */
void state_copy(int* new_state, int* prev_state){
	int i;
	for (i = 0; i < TILE_LEN; i++) {
		new_state[i] = prev_state[i];
	}
}

/* return the sum of manhattan distances from state to goal */
int manhattan( int* state )
{
	int sum = 0;
	int row,col,x,y;
	int index;
	for (col = 0; col < COL_LEN; col++) {
		for (row = 0; row < ROW_LEN; row++) {
			index = (col * COL_LEN) + row;
			// Manhattan Distance 1D -> 2D excluding Blank Tile
			if (state[index] != BLANK_TILE) {
				y = state[index] / COL_LEN;
				x = state[index] - (y * ROW_LEN);
				sum += abs(row - x) + abs(col - y);
			}
		}
	}

	return( sum );
}


/* return 1 if op is applicable in state, otherwise return 0 */
int applicable( int op )
{
    return( ap_ops[op][blank_pos] );
}


/* apply operator */
void apply( node* n, int op )
{
	int t;

	//find tile that has to be moved given the op and blank_pos
	t = blank_pos + (op == LEFT ? -1 : (op == RIGHT ? 1 : (op == UP ? -4 : 4)));

	//apply op
	n->state[blank_pos] = n->state[t];
	n->state[t] = BLANK_TILE;
	
	//update blank pos
	blank_pos = t;
}

// Finds the position of the blank tile given the state
void find_blank_pos(int* state) {
	int i;
	for (i = 0; i < TILE_LEN; i++) {
		if (state[i] == BLANK_TILE) {
			blank_pos = i;
			break;
		}
	}
}	

/* Recursive IDA */
node* ida( node* node, int threshold, int* newThreshold )
{
	int a;
	int estimate;
	int actions[MOVES] = {};
	struct node* r = NULL;
	struct node new_node;

	// Find out all the applicable moves in the current state
	for (a = 0; a < MOVES; a++) {
		actions[a] = applicable(a);
	}

	// Apply applicable moves
	for (a = 0; a < MOVES; a++) {
		if (actions[a] != 0 && a != node->prev_move) {
								// OPTIMIZATION - Last Moves Heuristic //
			/**************************************************************************************/
			new_node.prev_move = (a == LEFT ? RIGHT : (a == RIGHT ? LEFT : (a == UP ? DOWN : UP)));
			/**************************************************************************************/

			generated++;

			// Find the position of the blank tile
			find_blank_pos(node->state);

			state_copy(new_node.state, node->state);
			apply(&new_node, a);

			// Add 1 cost
			new_node.g = node->g + 1;

			// New estimated cost
			estimate = manhattan(new_node.state);
			new_node.f = new_node.g + estimate;

			// If estimated cost is greater than threshold
			if (new_node.f > threshold) {
				expanded++;
				if (new_node.f < *newThreshold) {
					// Update temporary threshold
					*newThreshold = new_node.f;
				}
			}
			else {
				if (estimate == 0) {
					// Yay we have reached the goal node
					r = &new_node;
					return r;
				}
				r = ida(&new_node, threshold, newThreshold);
				if (r != NULL) {
					return r;
				}
			}

		}
	}
	return( NULL );
}


/* main IDA control loop */
int IDA_control_loop(  ){
	struct node* r = NULL;
	
	int threshold;
	
	/* initialize statistics */
	generated = 0;
	expanded = 0;

	/* compute initial threshold B */
	initial_node.f = threshold = manhattan( initial_node.state );

	printf( "Initial Estimate = %d\nThreshold = ", threshold );
	printf("%d ", threshold);

	// While r is not NULL
	while (r == NULL) {
		// Threshold -> infinity
		int newThreshold = INT_MAX;
		struct node curr_node;
		
		// Node state = initial state
		state_copy(curr_node.state, initial_node.state);

		// Cost = 0
		curr_node.g = 0;
		curr_node.prev_move = 0;
		
		r = ida(&curr_node, threshold, &newThreshold);
		if (r == NULL) {
			// Update threshold
			threshold = newThreshold;
			printf("%d ", newThreshold);
		}
	}

	if(r)
		return r->g;
	else
		return -1;
}


static inline float compute_current_time()
{
	struct rusage r_usage;
	
	getrusage( RUSAGE_SELF, &r_usage );	
	float diff_time = (float) r_usage.ru_utime.tv_sec;
	diff_time += (float) r_usage.ru_stime.tv_sec;
	diff_time += (float) r_usage.ru_utime.tv_usec / (float)1000000;
	diff_time += (float) r_usage.ru_stime.tv_usec / (float)1000000;
	return diff_time;
}

int main( int argc, char **argv )
{
	int i, solution_length;

	/* check we have a initial state as parameter */
	if( argc != 2 )
	{
		fprintf( stderr, "usage: %s \"<initial-state-file>\"\n", argv[0] );
		return( -1 );
	}


	/* read initial state */
	FILE* initFile = fopen( argv[1], "r" );
	char buffer[256];

	if( fgets(buffer, sizeof(buffer), initFile) != NULL ){
		char* tile = strtok( buffer, " " );
		for( i = 0; tile != NULL; ++i )
			{
				initial_node.state[i] = atoi( tile );
				blank_pos = (initial_node.state[i] == 0 ? i : blank_pos);
				tile = strtok( NULL, " " );
			}		
	}
	else{
		fprintf( stderr, "Filename empty\"\n" );
		return( -2 );

	}
       
	if( i != 16 )
	{
		fprintf( stderr, "invalid initial state\n" );
		return( -1 );
	}

	/* initialize the initial node */
	initial_node.g=0;
	initial_node.f=0;

	print_state( initial_node.state );


	/* solve */
	float t0 = compute_current_time();
	
	solution_length = IDA_control_loop();				

	float tf = compute_current_time();

	/* report results */
	printf( "\nSolution = %d\n", solution_length);
	printf( "Generated = ");
	printf_comma(generated);		
	printf("\nExpanded = ");
	printf_comma(expanded);		
	printf( "\nTime (seconds) = %.2f\nExpanded/Second = ", tf-t0 );
	printf_comma((unsigned long int) expanded/(tf+0.00000001-t0));
	printf("\n\n");

	/* aggregate all executions in a file named report.dat for results */
	FILE* report = fopen( "report.dat", "a" );

	fprintf( report, "%s", argv[1] );
	fprintf( report, "\n\tSoulution = %d, Generated = %lu, Expanded = %lu", solution_length, generated, expanded);
	fprintf( report, ", Time = %f, Expanded/Second = %f\n\n", tf-t0, (float)expanded/(tf-t0));
	fclose(report);
	fclose(initFile);
	
	return( 0 );
}


