// CAS_CADE.c
// Commandline Accessable Simple C-lang-Assembler Developed by Epinephrine00
// cas_cade "Path_of_Your_ASM_File.asm"
// cas_cade "Path_of_Your_ASM_File.asm" "Path_of_Output_OBJE_File.obje"
// Recommended Output File Extension : *.obje (OBJect defined by Epinephrine00)

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
str* MRIs;
str outputFilePath;


void FirstPass(int count, str* lines);
void SecondPass(int count, str* lines);
void initOutputFile();
void writeFile(int instruction);
void freeLabelDict();
void pass(){return;}

int find(str line, char c);
int findDict(str key);
int lenDict();

str strip(str line);
str strupr(str line);
str in2out(str filename);

bool labelIncluded(str line);
bool isORG(str line);
bool isEND(str line);
bool isPseudoInstruction(str line);
bool isMRInstruction(str line);
bool isValidNonMRInstruction(str line);




int main(int argc, str argv[]){
    FILE* fd;
    char line[MAX_LEN];

    str* lines = NULL;
    int count = 0;
    int max_lines = INITIAL_MAX_LINES;
    labelDict = (struct str2intDict *)malloc(INITIAL_MAX_LINES * sizeof(struct str2intDict));
    MRIs = (str *)malloc(7 * sizeof(str));
    outputFilePath = (str)malloc(MAX_LEN*sizeof(char));
    if (MRIs == NULL || outputFilePath == NULL){
        perror("Memory allocation error");
        return 1;
    }
    MRIs[0] = "AND"; MRIs[1] = "ADD"; MRIs[2] = "LDA"; MRIs[3] = "STA"; MRIs[4] = "BUN"; MRIs[5] = "BSA"; MRIs[6] = "ISZ";

    if (labelDict == NULL){
        perror("Memory allocation error");
        return 1;
    }
    for (int i = 0; i < INITIAL_MAX_LINES; i++) {
        labelDict[i].key = NULL;//(str)malloc(MAX_LEN * sizeof(char));
        labelDict[i].value = 0;
    }

    ////printf("-- Debug : Program Successfuly Initialized and Started!\n\n");

    if (argc > 1) {
        if (argc>2){
            outputFilePath = argv[2];
        }
        else{
            outputFilePath = in2out(argv[1]);
        }
        initOutputFile();
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
        
        //printf("-- Debug : printing ASM code\n");
        //printf("-- Debug : count = %d\n", count);
        for (int i = 0; i < count; i++) {
        //    printf("%s || %d\n", lines[i], i);
        }
        //printf("-- Debug : ASM code Printed\n");
    }
    //printf("-- Debug : Calling First Pass\n");
    FirstPass(count, lines);

    for (int i = 0; i < count; i++) {
        free(lines[i]);
    }
    free(lines); 
    freeLabelDict();
    return 0;
}

void freeLabelDict(){
    for(int i=0; i<INITIAL_MAX_LINES; i++) free(labelDict[i].key);
    free(labelDict);
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

str strupr(str line){
    for(int i=0;i<strlen(line);i++) if((int)line[i]>0x60 && (int)line[i]<0x7B) line[i]-=0x20;
    return line;
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
        //printf("-- Debug : findDict(%s) |  labelDict[%d].key = %s  |  strcmp(labelDict[i].key, key) = %d\n", key, i, labelDict[i].key, strcmp(labelDict[i].key, key));
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
    //printf("-- Debug : Function labelIncluded : line = %s  | cond = %d\n", line, cond);
    if(cond==-1){free(label);return false;}
    for(int i=0; i<cond; i++) label[i] = line[i];
    //printf("-- Debug : Function labelIncluded : label = %s  |  findDict(label) = %d\n", label, findDict(label));
    if(findDict(label)==-1){
        //printf("-- Debug : Function labelIncluded : key = %s  |  value = %d  |  labelCount = %d\n", label, LC, labelCount);
        //for(int i = 0; i<strlen(label); i++) labelDict[labelCount].key[i] = label[i];
        //strcpy(labelDict[labelCount].key, label);
        labelDict[labelCount].key = label;
        labelDict[labelCount].value = LC;
        labelCount++;
        //printf("                                  : key = %s  |  value = %d  |  labelCount = %d\n", labelDict[labelCount-1].key, labelDict[labelCount-1].value, labelCount);
    }
    //free(label);
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
        free(instruction);
        free(address);
        return true;
    }
    free(instruction);
    free(address);
    return false;
}

bool isEND(str line){
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    for(int i=0; i<3; i++) instruction[i] = line[i];
    if(strcmp(instruction, "END")==0){free(instruction); return true;}
    free(instruction);
    return false;
}

void FirstPass(int count, str* lines){
    LC = 0;
    //printf("-- Debug : First Pass Begin\n");
    for(int i = 0; i < count; i++){
        if(labelIncluded(lines[i])) LC++;
        else if(isORG(lines[i])) continue;
        else if(isEND(lines[i])){break; return;}
        else LC++;
        //printf("%s  |  LC : %d\n", lines[i], LC);
    }
    //printf("%d\n", lenDict());
    //printf("%d\n", LC);
    //for(int i=0; i<lenDict(); i++){
    //    printf("%s : %d\n", labelDict[i].key, labelDict[i].value);
    //}

    //printf("-- Debug : First Pass Finished. Calling Second Pass...\n");
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


str in2out(str filename){
    str result = (str)malloc(MAX_LEN * sizeof(char));
    int dot = find(filename, '.');
    for(int i=0; i<dot; i++) result[i] = filename[i];
    result[dot] = '.';
    result[dot+1] = 'o';
    result[dot+2] = 'b';
    result[dot+3] = 'j';
    result[dot+4] = 'e';
    //obje : OBJect defined by Epinephrine00 / 다시 말씀드리지만 Epinephrine00은 제 닉네임입니다.
    return result;
}


bool isPseudoInstruction(str line){
    str label = (str)malloc(MAX_LEN * sizeof(char));
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    str address = (str)malloc(MAX_LEN * sizeof(char));
    str delabeled = (str)malloc(MAX_LEN * sizeof(char));
    int labelends = find(line, ',');
    long value = 0;
    delabeled = delabeler(line);
    instruction = getInstruction(line);
    if(labelends==-1) label = NULL;
    else for(int i=0; i<labelends; i++) label[i] = line[i];
    for(int i=4; i<strlen(delabeled); i++) address[i-4] = delabeled[i];
    if(strcmp(instruction, "ORG")==0){
        LC = atoi(address);
        goto returntrue;
    }
    else if(strcmp(instruction, "END")==0){
        secondPassStopFlag = true;
        goto returntrue;
    }
    else if(strcmp(instruction, "HEX")==0){
        printf("-- Debug : Hex %s = %ld\n", address, strtol(address, NULL, 16));
        value = strtol(address, NULL, 16);
        writeFile(value);
        LC++;
        goto returntrue;
    }
    else if(strcmp(instruction, "DEC")==0){
        printf("-- Debug : Dec %s = %d\n", address, atoi(address));
        value = atoi(address);
        writeFile(value);
        LC++;
        goto returntrue;
    }
    return false;
returntrue: // 스파게티코드 만들기
    free(label);
    free(instruction);
    free(address);
    free(delabeled);
    return true;
}

bool isMRInstruction(str line){
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    str address = (str)malloc(MAX_LEN * sizeof(char));
    str delabeled = (str)malloc(MAX_LEN * sizeof(char));
    instruction = getInstruction(line);
    delabeled = delabeler(line);
    bool isI = false;
    for(int i=4; i<strlen(delabeled); i++){
        if(delabeled[i]!=' ' && isI==false) address[i-4] = delabeled[i];
        else isI = true;
        // line은 strip된 문자열로 들어오므로, ADD A I와 같이 메모리 주소 뒤에 ' ' 기호가 있다면 간접주소방식이라고 판단함. 그 뒤에 뭐가오든 관심없음.
    }
    int result = 0x0000;
    for(int i=0; i<7; i++){
        if(strcmp(instruction, MRIs[i])==0){
            result |= i<<12;
            result |= labelDict[findDict(address)].value&0x0FFF;
            result |= (int)isI<<15;
            goto itsMRInstruction;
        }
    }
    return false;
itsMRInstruction: // 프로 스파게티 요리사
    //LC 위치에 result를 저장
    printf("Instruction : %X, %d, \n", result, result);
    writeFile(result);
    free(instruction); free(address); free(delabeled);
    LC++;
    return true;
}

bool isValidNonMRInstruction(str line){
    str instruction = (str)malloc(MAX_LEN * sizeof(char));
    instruction = getInstruction(line);
    int result = -1;
    if(strcmp(instruction, "CLA")==0) result = 0x7800;
    else if(strcmp(instruction, "CLE")==0) result = 0x7400;
    else if(strcmp(instruction, "CMA")==0) result = 0x7200;
    else if(strcmp(instruction, "CME")==0) result = 0x7100;
    else if(strcmp(instruction, "CIR")==0) result = 0x7080;
    else if(strcmp(instruction, "CIL")==0) result = 0x7040;
    else if(strcmp(instruction, "INC")==0) result = 0x7020;
    else if(strcmp(instruction, "SPA")==0) result = 0x7010;
    else if(strcmp(instruction, "SNA")==0) result = 0x7008;
    else if(strcmp(instruction, "SZA")==0) result = 0x7004;
    else if(strcmp(instruction, "SZE")==0) result = 0x7002;
    else if(strcmp(instruction, "HLT")==0) result = 0x7001;
    else if(strcmp(instruction, "INP")==0) result = 0xF800;
    else if(strcmp(instruction, "OUT")==0) result = 0xF400;
    else if(strcmp(instruction, "SKI")==0) result = 0xF200;
    else if(strcmp(instruction, "SKO")==0) result = 0xF100;
    else if(strcmp(instruction, "ION")==0) result = 0xF080;
    else if(strcmp(instruction, "IOF")==0) result = 0xF040;
    if(result == -1){
        LC++;
        return false;
    }
    else{
        //LC 위치에 result를 저장하는 코드 추가할것
        printf("Instruction : %X, %d\n", result, result);
        writeFile(result);
        LC++;
        return true;
    }
}

void initOutputFile(){
    FILE* fd;
    fd = fopen(outputFilePath, "w");
    fclose(fd);
    //printf("filename : %s\n", outputFilePath);
    return;
}

void writeFile(int instruction){
    // LC 위치에 명령어를 올리는게 그.... 어셈블러가 직접 올릴 일은 아니니까
    // LC와 Instruction을 각각 한줄에 저장해서...
    // 로더(Loader)..?를 구현해 걔가 메모리에 적재하고 실행까지 시키도록 구현하겠습니다
    FILE* fd;
    fd = fopen(outputFilePath, "a");
    fprintf(fd, "%04X%04X", LC, instruction);
    fclose(fd);
    pass();
}


void SecondPass(int count, str* lines){
    LC = 0;
    ////printf("-- Debug : Second Pass Begin\n");

    for(int i=0; i<count; i++){
        if(isPseudoInstruction(lines[i])){
            if(secondPassStopFlag) break;
            else continue;
        }
        else if(isMRInstruction(lines[i])){
            pass();
        }
        else if(isValidNonMRInstruction(lines[i])){
            pass();
        }
        else{
            perror("Invalid Instruction");
            freeLabelDict();
            free(lines);
            // free(everythingElse);
            return;
        }

        
    }
    return;
}

// 코드 길이가 고작 이거밖에 안돼??
// 어셈블러 어려울줄알았더니 별거 아니네