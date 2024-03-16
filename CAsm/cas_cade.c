// CAS_CADE.c
// Commandline Accessable Simple C-lang-Assembler Developed by Epinephrine00
// cas_cade "Path_of_Your_ASM_File.asm" 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 128
#define INITIAL_MAX_LINES 4096


int LC;

void FirstPass(int count, char** lines);
char* strip(char* line);
int find(char* line, char c);
bool isLabelIncluded(char* line);



int main(int argc, char* argv[]){
    FILE* fd;
    char line[MAX_LEN];
    char** lines = NULL;
    int count = 0;
    int max_lines = INITIAL_MAX_LINES;

    printf("HEllow!, Wodlsre?\n\n");

    if (argc > 1) {
        fd = fopen(argv[1], "r");
        if (fd == NULL) {
            perror("Error opening file");
            return 1;
        }
        lines = (char**)malloc(max_lines * sizeof(char*));
        if (lines == NULL) {
            perror("Memory allocation error");
            fclose(fd);
            return 1;
        }

        while (fgets(line, MAX_LEN, fd) != NULL) {
            lines[count] = strdup(strip(line));
            if (lines[count] == NULL) {
                perror("Memory allocation error");
                fclose(fd);
                for (int i = 0; i < count; ++i)
                    free(lines[i]);
                free(lines);
                return 1;
            }
            count++;


            if (count >= max_lines) {
                max_lines *= 2;
                char** temp = realloc(lines, max_lines * sizeof(char*));
                if (temp == NULL) {
                    perror("Memory reallocation error");
                    fclose(fd);
                    for (int i = 0; i < count; ++i)
                        free(lines[i]);
                    free(lines);
                    return 1;
                }
                lines = temp;
            }
        }
        fclose(fd);
        

        for (int i = 0; i < count; i++) {
            printf("%s\n", lines[i]);
        }
    }

    FirstPass(count, lines);

    for (int i = 0; i < count; i++) {
        free(lines[i]); // 메모리 해제
    }
    free(lines); // 포인터 배열을 가리키는 메모리 해제
    
    return 0;
}

char* strip(char* line){
    char* result;
    int s = 0, e = strlen(line)-1;
    while(line[s]==' ' || line[s]=='\n') s++;
    while(line[e]==' ' || line[e]=='\n') e--;
    //printf("%s %d %d\n", line, s, e);
    result = (char*)malloc(((e-s)+1) * sizeof(char));
    for(int i = s; i<=e; i++)result[i-s]=line[i];
    return result;
}

int find(char* line, char c){
    char* result;
    int s = 01;
    for(;s<strlen(line);s++) if(line[s]==c) return s;
    return -1;
}

bool isLabelIncluded(char* line){

}

void FirstPass(int count, char** lines){
    LC = 0;

    for(int i = 0; i < count; i++){
        //printf("%s | %ld\n",lines[i], strlen(lines[i]));
        
        printf("\n");
    }

    return;
}