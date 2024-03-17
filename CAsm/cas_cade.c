// CAS_CADE.c
// Commandline Accessable Simple C-lang-Assembler Developed by Epinephrine00
// cas_cade "Path_of_Your_ASM_File.asm" 

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 128
#define INITIAL_MAX_LINES 4096

typedef enum{false=0, true=1} bool;
typedef char* str;

struct str2intDict{
    str key;
    int value;
} str2intDict;

int LC;
int labelCount;
bool secondPassStopFlag = false;

struct str2intDict* labelDict;


void FirstPass(int count, str* lines);
void SecondPass(int count, str* lines);
str strip(str line);
int find(str line, char c);
bool labelIncluded(str line);
int findDict(str key);
int lenDict();
bool isORG(str line);
bool isEND(str line);
str strupr(str line);



int main(int argc, str argv[]){
    FILE* fd;
    char line[MAX_LEN];

    str* lines = NULL;
    int count = 0;
    int max_lines = INITIAL_MAX_LINES;
    labelDict = (struct str2intDict *)malloc(INITIAL_MAX_LINES * sizeof(struct str2intDict));
    if (labelDict == NULL){
        perror("Memory allocation error");
        return 1;
    }
    for (int i = 0; i < INITIAL_MAX_LINES; i++) {
        labelDict[i].key = NULL;
        labelDict[i].value = 0;
    }

    printf("-- Debug : Program Successfuly Initialized and Started!\n\n");

    if (argc > 1) {
        fd = fopen(argv[1], "r");
        if (fd == NULL) {
            perror("Error opening file");
            return 1;
        }
        lines = (str*)malloc(max_lines * sizeof(str));
        if (lines == NULL) {
            perror("Memory allocation error");
            fclose(fd);
            return 1;
        }


        while (fgets(line, MAX_LEN, fd) != NULL) {
            lines[count] = strdup(strupr(strip(line)));
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
                str* temp = realloc(lines, max_lines * sizeof(str));
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
        
        printf("-- Debug : printing ASM code\n");
        printf("-- Debug : count = %d\n", count);
        for (int i = 0; i < count; i++) {
            printf("%s || %d\n", lines[i], i);
        }
        printf("-- Debug : ASM code Printed\n");
    }
    printf("-- Debug : Calling First Pass\n");
    FirstPass(count, lines);

    for (int i = 0; i < count; i++) {
        free(lines[i]);
    }
    free(lines); 
    free(labelDict);
    
    return 0;
}

str strip(str line){
    str result;
    int s = 0, e = strlen(line)-1;
    while(line[s]==' ' || line[s]=='\n') s++;
    while(line[e]==' ' || line[e]=='\n') e--;
    //printf("%s %d %d\n", line, s, e);
    result = (str)malloc(((e-s)+1) * sizeof(char));
    for(int i = s; i<=e; i++)result[i-s]=line[i];
    return result;
}

int find(str line, char c){
    str result;
    int s = 01;
    for(;s<strlen(line);s++) if(line[s]==c) return s;
    return -1;
}

int findDict(str key){
    int i = 0;
    while(labelDict[i].key!=NULL){
        if(strcmp(labelDict[i].key, key)==0) return i;
        i++;
    }
    return -1;
}

int lenDict(){
    int i = 0;
    while(labelDict[i].key!=NULL) i++;
    return i;
}

bool labelIncluded(str line){
    str label = (str)malloc(MAX_LEN * sizeof(char));;
    int cond = find(line, ',');
    if(cond==-1) return false;
    for(int i=0; i<cond; i++) label[i] = line[i];
    if(findDict(label)==-1){
        labelDict[labelCount].key = label;
        labelDict[labelCount].value = LC;
        labelCount++;
    }
    return true;
}

bool isORG(str line){
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    str address = (str)malloc(MAX_LEN * sizeof(char));
    for(int i=0; i<3; i++) instruction[i] = line[i];
    for(int i=4; i<strlen(line); i++) address[i-4] = line[i];
    //printf("%s : isORG = %d  | address = %s\n", instruction, strcmp(instruction, "ORG"), address);
    if(strcmp(instruction, "ORG")==0){
        LC = atoi(address);
        return true;
    }
    return false;
}

bool isEND(str line){
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    for(int i=0; i<3; i++) instruction[i] = line[i];
    if(strcmp(instruction, "END")==0) return true;
    return false;
}

str strupr(str line){
    for(int i=0;i<strlen(line);i++) if((int)line[i]>0x60 && (int)line[i]<0x7B) line[i]-=0x20;
    return line;
}

void FirstPass(int count, str* lines){
    LC = 0;
    printf("-- Debug : First Pass Begin\n");
    for(int i = 0; i < count; i++){
        if(labelIncluded(lines[i])) LC++;
        else if(isORG(lines[i])) continue;
        else if(isEND(lines[i])){break; return;}
        else LC++;
        printf("%s  |  LC : %d\n", lines[i], LC);
    }
    printf("%d\n", lenDict());
    printf("%d\n", LC);
    for(int i=0; i<lenDict(); i++){
        printf("%s : %d\n", labelDict[i].key, labelDict[i].value);
    }

    printf("-- Debug : First Pass Finished. Calling Second Pass...\n");
    SecondPass(count, lines);

    return;
}

str delabeler(str line){
    int cond = find(line, ',');
    if(cond==-1) return strip(line);
    str result = (str)malloc(MAX_LEN * sizeof(char));
    for(int i=cond+1; i<strlen(line); i++) result[i-(cond+1)] = line[i];
    return strip(result);
}

str getInstruction(str line){
    str result = (str)malloc(MAX_LEN * sizeof(char));
    str delabeled = (str)malloc(MAX_LEN * sizeof(char));
    delabeled = delabeler(line);
    for(int i=0; i<3; i++) result[i] = delabeled[i];
    return result;
}


bool isPseudoInstruction(str line){
    str label = (str)malloc(MAX_LEN * sizeof(char));
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    str address = (str)malloc(MAX_LEN * sizeof(char));
    str delabeled = (str)malloc(MAX_LEN * sizeof(char));
    int labelends = find(line, ',');
    delabeled = delabeler(line);
    instruction = getInstruction(line);
    if(labelends==-1) label = NULL;
    else for(int i=0; i<labelends; i++) label[i] = line[i];
    for(int i=4; i<strlen(delabeled); i++) address[i-4] = delabeled[i];
    if(strcmp(instruction, "ORG")==0){
        LC = atoi(address);
        return true;
    }
    else if(strcmp(instruction, "END")==0){
        secondPassStopFlag = true;
        return true;
    }
    else if(strcmp(instruction, "HEX")==0){
        // 값 넣는 내용 추가할것
        LC++;
        return true;
    }
    else if(strcmp(instruction, "DEC")==0){
        // 값 넣는 내용 추가할것
        LC++;
        return true;
    }
    return false;
}


void SecondPass(int count, str* lines){
    LC = 0;
    printf("-- Debug : Second Pass Begin\n");

    for(int i=0; i<count; i++){
        if(isPseudoInstruction(lines[i])){
            if(secondPassStopFlag) break;
            else continue;
        }
        else if(isMRInstruction(lines[i])){
            //asdf;
        }

        
    }
    return;
}