
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

struct Info {
	int numWords;
	char ** wordArr;
};

//ret negative if a < b, 0 if a == b, positive if a > b
int frobcmp(const void * a1, const void * b1) {
	
	const char * a = *(const char **) a1;
	const char * b = *(const char **) b1;
	int i = 0;
	while (a[i] != ' ' && b[i] != ' ')
	{
		if ( (a[i] ^ 42) > (b[i] ^ 42) )
			return 1;
		else if ( (a[i] ^ 42) < (b[i] ^ 42) )
		{	
			return -1;
		}
		i++;
	}
	if (a[i] == ' ' && b[i] != ' ') //a shorter
	{
		return -1;
	}
	else if (a[i] != ' ' && b[i] == ' ') //b shorter
		return 1;
	return 0; //strings ==
}

void errors(int i)
{
	switch(i) {
		case 0:
			fprintf(stderr, "malloc failed\n");
			break;
		case 1:
			fprintf(stderr, "realloc failed\n");
			break;
		case 2:
			fprintf(stderr, "I/O error\n");
			break;
	}
	exit(1);
}

void freeAll(char **ptr, int wordCount) {
	int i;
	for (i = 0; i < wordCount; i++)
		free(ptr[i]);
	free(ptr);	
}

struct Info* strings() { 
	char ** strarr,** holder1;
	char * holder2;
	int wordCount;	//keep track of # of strings
	strarr = (char**)malloc(sizeof(char*)); 	//allocate 1 string to start
	if (strarr == NULL)
		errors(0);
	wordCount = 0;
	while (!feof(stdin))
	{
		holder1 = realloc(strarr, (wordCount+2)*sizeof(char*));
		if (holder1 == NULL)
		{
			freeAll(strarr, wordCount + 1);
			errors(1);
		}
		strarr = holder1;
		strarr[wordCount] = malloc(sizeof(char));	//1 char to start
		if (strarr[wordCount] == NULL)
		{	
			freeAll(strarr, wordCount + 1);
			errors(0);
		}
		int index;
		for (index = 0; !feof(stdin); index++)
		{
			holder2 = (char *) realloc(strarr[wordCount], 
									(index + 2) * sizeof(char));
			if (holder2 == NULL)
			{
				freeAll(strarr, wordCount + 1);
				errors(1);
			}
			strarr[wordCount] = holder2;
			char c = getchar();
			if (ferror(stdin))
				errors(2);
			if (c == EOF)
			{
				strarr[wordCount][index] = ' ';
				break;
			}
			strarr[wordCount][index] = c;
			if (c == ' ')
				break;
		} 
		wordCount++;
	}
	struct Info* x = malloc(sizeof(struct Info));
	if (x == NULL)
	{
		freeAll(strarr, wordCount); 
		errors(0);
	}
	x->numWords = wordCount;
	x->wordArr = strarr;
	return x;
}

int main() {
	struct Info *a = strings();
	qsort(a->wordArr, a->numWords, sizeof(char *), frobcmp);
	int i, j;
	for (i = 0; i < a->numWords; i++)
	{
		for(j=0; a->wordArr[i][j] != ' '; j++)
			putchar(a->wordArr[i][j]);
		putchar(' ');
	}
	freeAll(a->wordArr, a->numWords);
	free(a);
	exit(0);
}

