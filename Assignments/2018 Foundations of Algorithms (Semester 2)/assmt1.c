/* Extended precision integer calculator
 * Implements +, *, and ^ (power of) operations
 *
 * Skeleton code written by Jianzhong Qi, March 2018
 * Rest of the code writtten by Akira Wang, April 2018 (Student ID 913391)
 */
/* Algorithms are fun */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define INT_SIZE	100	/* max number of digits per integer value */
#define LINE_LEN	103	/* maximum length of any input line */
#define NUM_VARS	10	/* number of different huge int "variables" */

#define ASN_OP		'='	/* assignment operator */
#define ECH_OP		'?'	/* echo operator */
#define ADD_OP		'+'	/* addition operator */
#define MUL_OP		'*'	/* multiplication operator */
#define POW_OP		'^'	/* power of operator */

#define OPR1_POS	1	/* position of the first operand */
#define OPR2_POS	3	/* position of the second operand */
#define OP_POS		2	/* position of the operator */

#define CH_ZERO		'0'	/* character 0 */

#define EXIT_CMD 	"exit"	/* command to exit */
#define PROMPT		"> "	/* command prompt */
#define CMT_FLAG	'%'		/* indicator for comment line */

typedef int huge_t[INT_SIZE];	/* one huge int "variable" */
typedef int digit_t;			/* a decimal digit */

/* add your constant and type definitions here */
#define MAX_INT_SIZE	200 /* max length of 100digits*100digits = 200digits */
#define CARRY_LIM       10  /* the tens column in a number */
/****************************************************************/

/* function prototypes */
void read_line(char *line, int max_len);
void init(huge_t vars[], int lens[]); 
void echo(huge_t vars[], int lens[], int opr1_index);
void assign(huge_t vars[], int lens[], int opr1_index, char *opr2_str);
void add(huge_t vars[], int lens[], int opr1_index, char *opr2_str);
void multiply(huge_t vars[], int lens[], int opr1_index, char *opr2_str);
void power(huge_t vars[], int lens[], int opr1_index, char *opr2_str);

/* add your function prototypes here */
void max_size_check(int lens[], int opr1_index);
void zero_array_check(huge_t vars[], int lens[], int opr1_index);
void remove_leading_zeros(huge_t vars[], int lens[], int opr1_index);
/****************************************************************/

/* main function controls all the action, do NOT modify this function */
int
main(int argc, char *argv[]) {
	char line[LINE_LEN+1];		/* to hold the input line */
	huge_t vars[NUM_VARS];		/* to hold 10 huge integers */
	int lens[NUM_VARS];			/* to hold the length of the 10 vars */
	
	int opr1_index;				/* index of the first operand in command */
	char op;					/* operator in command */
	
	init(vars, lens);
	
	while (1) {
		printf(PROMPT);						/* print prompt */
		read_line(line, LINE_LEN);			/* read one line of command */

		if (line[0] == CMT_FLAG) {			/* print comment in the test data */ 
			printf("%s\n", line);			/* used to simplify marking */
			continue;
		}
		
		if (strcmp(line, EXIT_CMD) == 0) {	/* see if command is "exit" */
			return 0;
		} 
		
		opr1_index = line[OPR1_POS] - CH_ZERO;/* first var number at line[1] */
		op = line[OP_POS];					/* operator at line[2] */

		if (op == ECH_OP) {					/* print out the variable */
			echo(vars, lens, opr1_index);
			continue;
		} 
		
		/* do the calculation, second operand starts at line[3] */
		if (op == ASN_OP) {	
			assign(vars, lens, opr1_index, line+OPR2_POS);
		} else if (op == ADD_OP) {
			add(vars, lens, opr1_index, line+OPR2_POS);
		} else if (op == MUL_OP) {
			multiply(vars, lens, opr1_index, line+OPR2_POS);
		} else if (op == POW_OP) {
			power(vars, lens, opr1_index, line+OPR2_POS);
		}
	}
	
	/* all done; take some rest */
	return 0;
}

/* read a line of input into the array passed as argument */
void
read_line(char *line, int max_len) {
	int i = 0, c;
	while (((c = getchar()) != EOF) && (c != '\n') && (c != '\r')) {
		if (i < max_len) {
			line[i++] = c;
		} else {
			printf("Invalid input line, toooooooo long.\n");
			exit(0);
		}
	}
	line[i] = '\0';
}

/* print out a huge integer */
void echo(huge_t vars[], int lens[], int opr1_index) {
	int i;

	/* print the digits in a reverse order */
	for (i = lens[opr1_index]-1; i >= 0; i--) {
		printf("%d", vars[opr1_index][i]);
	}
	
	printf("\n");
}


/****************************************************************/

/* add code below to complete the function bodies,
 * add more functions where appropriate.
 */

/* set the vars array to zeros */
void
init(huge_t vars[], int lens[]) {
    int i, j;
	for(i = 0; i < NUM_VARS; i++) {
	    for(j = 0; j < INT_SIZE; j++) {
		    vars[i][j] = 0;
	    }
	    lens[i] = 1;    /* set length of array to 1 */
	}
}

/* function check to see if the length has exceeded 100 digits */
void
max_size_check(int lens[], int opr1_index) {
	if (lens[opr1_index] > INT_SIZE) { 							
		lens[opr1_index] = INT_SIZE;
	}
}

/* function check to see if the array is just 0's */
void 
zero_array_check(huge_t vars[], int lens[], int opr1_index) {
    int i, check = 0;
    /* the sum of all 0's is 0 so if check = 0, then the output is 0's */
    for (i = 0; i < lens[opr1_index]; i++) {
        check += vars[opr1_index][i];
    }
    if (!check) {
        lens[opr1_index] = 1;
    }
}

/* function to remove any leading zeros */
void
remove_leading_zeros(huge_t vars[], int lens[], int opr1_index) {
    /* remove any leading 0's that occur */
    while (vars[opr1_index][lens[opr1_index] - 1] == 0) {
        lens[opr1_index]--;
    }
}

/* process the '=' operator */
void
assign(huge_t vars[], int lens[], int opr1_index, char *opr2_str) {
    int i, j;

    /* re-init the variable if it has been previously used*/
    if (lens[opr1_index] != 1) {
        for (i = 0; i < INT_SIZE; i++) {
            vars[opr1_index][i] = 0;
        }
    }
    /* if the input is a digit */
    if (isdigit(opr2_str[0])) {
        lens[opr1_index] = strlen(opr2_str);  /* equate lengths of the number */
        j = strlen(opr2_str) - 1; 		/* append array in reverse order */
        for(i = 0; i < lens[opr1_index]; i++) {
            /* Force char into an int type */
            vars[opr1_index][i] = opr2_str[j] - CH_ZERO;
            j--;
        }
    }
	/* if the input is a variable */
    if (opr2_str[0] == 'n') {
        /* equate lengths of the variables */
        lens[opr1_index] = lens[opr2_str[1] - CH_ZERO];
        for(i = 0; i < lens[opr1_index]; i++) {
	        /* Force char into an int type */
	        vars[opr1_index][i] = vars[opr2_str[1] - CH_ZERO][i];
	    }   
    }
}

/* process the '+' operator */
void
add(huge_t vars[], int lens[], int opr1_index, char *opr2_str) {
    int i, j = 0, input_type_len;
    /* temporarily store the opr2_str in reversed order */
    /* I probably could have used assign but cbs it works I guess*/
    int reversed_opr2_str[INT_SIZE] = {0};
    /* if the input is a real number */
	
    if (isdigit(opr2_str[0])) { 						
	    input_type_len = strlen(opr2_str);
	    /* reverse the array to make adding easier*/
        for (i = input_type_len - 1; i >= 0; i--) {
            reversed_opr2_str[i] = opr2_str[j] - CH_ZERO;
            j++;
        }
    }
    /* if the input is a variable */
    if (opr2_str[0] == 'n') {
        input_type_len = lens[opr2_str[1] - CH_ZERO];
    }
    /* case for when the number of digits are greater than or equal */
    if (input_type_len >= lens[opr1_index]) {
        lens[opr1_index] = input_type_len;
    }
    if (lens[opr1_index] > input_type_len) {
        input_type_len = lens[opr1_index];
    }
    /* in case an extra digit is needed */
    lens[opr1_index]++;
    for (i = 0; i < input_type_len; i++) {
	    if (isdigit(opr2_str[0])) {		/* add the number */
            vars[opr1_index][i] += reversed_opr2_str[i];
	    }
	    if (opr2_str[0] == 'n') { 		/* add the variable */
	        vars[opr1_index][i] += vars[opr2_str[1] - CH_ZERO][i];
	    }
        if (vars[opr1_index][i] >= CARRY_LIM) { 	/* check for a carry */
            vars[opr1_index][i] -= CARRY_LIM;
            vars[opr1_index][i+1]++;
        }
    }
    max_size_check(lens, opr1_index);
    remove_leading_zeros(vars, lens, opr1_index);
    zero_array_check(vars, lens, opr1_index);
}

/* process the '*' operator */
void 
multiply(huge_t vars[], int lens[], int opr1_index, char *opr2_str) {
    int i, j = 0, carry = 0, input_type_len;
    int reversed_opr2_str[INT_SIZE];
    /* temporarily store the product with a hypothetical max len of 200 */
    int product[MAX_INT_SIZE] = {0};

    /* if the input is a real number */			
    if (isdigit(opr2_str[0])) {
	input_type_len = strlen(opr2_str);
	/* reverse the array to make multiplying easier*/
        for (i = input_type_len - 1; i >= 0; i--) {
            reversed_opr2_str[i] = opr2_str[j] - CH_ZERO;
            j++;
        }
	    lens[opr1_index] += input_type_len;
    }
    /* if input is a variable */
    if (opr2_str[0] == 'n') {
        input_type_len = lens[opr2_str[1] - CH_ZERO];
        lens[opr1_index] += input_type_len;
    }
    /* the (i+j)th digit is calculated by multiplying ith*jth */
    for (i = 0; i < input_type_len; i++) {
	    for (j = 0; j < lens[opr1_index]; j++) {
	        if (isdigit(opr2_str[0])) {
		        product[i+j] += reversed_opr2_str[i] * vars[opr1_index][j];
	        }
	        if (opr2_str[0] == 'n') {
		        product[i+j] += vars[opr2_str[1] - CH_ZERO][i] * vars[opr1_index][j];
	        }
	    }
    }
    /* check for carries */
    for (i = 0; i < input_type_len + lens[opr1_index]; i++) { 
        if ((product[i] / CARRY_LIM) != 0) {
	        carry = product[i] / CARRY_LIM;
	        product[i] = product[i] % CARRY_LIM;
            product[i+1] += carry;
	    }
    }
    max_size_check(lens, opr1_index);
    /* assign product to vars with a limit of 100 digits */
    for (i = 0; i < lens[opr1_index]; i++) {
	    vars[opr1_index][i] = product[i]; 
    }
    remove_leading_zeros(vars, lens, opr1_index);
    zero_array_check(vars, lens, opr1_index);
}

/* process the '^' operator */
void 
power(huge_t vars[], int lens[], int opr1_index, char *opr2_str) {
	int i, j, k, exponent = 0, carry = 0, digit_increase = 0;
	/* temporarily store the product with a hypothetical max len of 200 */
	int power_of[MAX_INT_SIZE] = {0};
	/* assuming all the power of operations 
	are up to two digits for my own sanity */
	if (isdigit(opr2_str[0])) { 
		if (strlen(opr2_str) == 2) {
			exponent += ((opr2_str[0] - CH_ZERO) * CARRY_LIM);
			exponent += opr2_str[1] - CH_ZERO;
		}
		else {
			exponent = opr2_str[0] - CH_ZERO;
		}
	}
	if (opr2_str[0] == 'n') {
		if (lens[opr2_str[1] - CH_ZERO] == 2) {
			exponent += ((vars[opr2_str[1] - CH_ZERO][1]) * CARRY_LIM);
			exponent += vars[opr2_str[1] - CH_ZERO][0];
		}
		else {
			exponent = vars[opr2_str[1] - CH_ZERO][0];
		}
	}
	/* if the power of holds value 0, then it must return 1 */
	if (exponent == 0) {
		lens[opr1_index] = 1;
		vars[opr1_index][0] = 1;
	}
	/* if the power of holds value 1, then it just returns itself */
	else if (exponent == 1) {
		/* do nothing */
	}
	else {
		digit_increase = lens[opr1_index];
		lens[opr1_index] += digit_increase;
		/* set the temp array to store the variable */
		for (j = 0; j < lens[opr1_index]; j++) {
			for (k = 0; k < lens[opr1_index]; k++) {
				/* init array by squaring it once */
				power_of[j+k] += vars[opr1_index][j] * vars[opr1_index][k];
			}
		}
		/* perform the power of operation until it reaches the power of 2 */
		/* since we have done it above already once when init'ing */
		for (i = exponent; i > 2; i--) {
			for (j = 0; j < lens[opr1_index]; j++) {
				power_of[j] *= vars[opr1_index][j];
			}
			lens[opr1_index] += digit_increase;
		}
		/* check for carries */
		for (i = 0; i < 2*lens[opr1_index]; i++) {
			if ((power_of[i] / CARRY_LIM) != 0) {
				carry = power_of[i] / CARRY_LIM;
				power_of[i] = power_of[i] % CARRY_LIM;
				power_of[i+1] += carry;
			}
		}
		max_size_check(lens, opr1_index);
		/* assign power_of to vars with a limit of 100 digits */
		for (i = 0; i < lens[opr1_index]; i++) {
			vars[opr1_index][i] = power_of[i];
		}
		remove_leading_zeros(vars, lens, opr1_index);
		zero_array_check(vars, lens, opr1_index);
	}
}