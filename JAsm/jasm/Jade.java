// JADE.java
// Java-Assembler Developed by Epinephrine00
// java jasm/Jade "Path_of_Your_ASM_File.asm"
// java jasm/Jade "Path_of_Your_ASM_File.asm" "Path_of_Output_OBJE_File.obje"
// Recommended Output File Extension : *.obje (OBJect defined by Epinephrine00)


package jasm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;
import jasm.Hash;

public class Jade {
    private String            outputFilename;
    private String[]          MRI             = new String[] {"AND", "ADD", "LDA", "STA", "BUN", "BSA", "ISZ"};
    private String[]          RRI             = new String[] {"CLA", "CLE", "CMA", "CME", "CIR", "CIL", "INC", "SPA", "SNA", "SZA", "SZE", "HLT"};
    private String[]          IOI             = new String[] {"INP", "OUT", "SKI", "SKO", "ION", "IOF"};
    private String[]          Pseudo          = new String[] {"ORG", "END", "DEC", "HEX"};
    private ArrayList<Hash>   SymbolTable     = new ArrayList<>();
    private ArrayList<String> code            = new ArrayList<>();
    private int               LC              = 0;
    private String            MLC             = new String();
    private void addMLC(int content) {this.MLC += String.format("%04X%04X", this.LC, content); return;}

    public Jade(String[] args){
        if(args.length>0){
            if(args.length>1){
                this.outputFilename = args[1];
            }
            else{
                this.outputFilename = args[0].substring(0,args[0].indexOf("."))+".obje";
            }
            try{this.fileReader(args[0]);}
            catch(IOException e){System.out.println(e.toString());return;}
        }
        else{
            return;
        }
    }

    public void compile(){
        this.firstPass();
        try{
            this.secondPass();
            this.saveOutputFile();
        }
        catch(Exception e){System.out.println(e.toString());return;}
        
        return;
    }

    private void fileReader(String filename) throws IOException{
        Scanner f = new Scanner(new File(filename));
        while(f.hasNextLine()){this.code.add(f.nextLine());}
    }

    private void firstPass(){
        this.LC = 0;
        for(String line : this.code){
            line = line.strip().toUpperCase();
            int div = line.indexOf(" ");
            String instruction = new String();
            String address = new String();
            if(div==-1){
                instruction = line;
                address = "";
            }
            else{
                instruction = line.substring(0,div);
                address = line.substring(div+1, line.length());
            }
            if(line.indexOf(",")!=-1){
                String label = line.substring(0,line.indexOf(","));
                boolean isIn = false; 
                for(Hash hash : this.SymbolTable){if(hash.getKey().equals(label)){isIn=true;}}
                if(!isIn){
                    this.SymbolTable.add(new Hash(label, this.LC));
                    this.LC++;
                }
            }
            else if(instruction.equals("ORG")){
                this.LC = Integer.parseInt(address);
            }
            else if(instruction.equals("END")){
                return;
            }
            else{
                this.LC++;
            }
        }
        
        return;
    }

    private void secondPass() throws Exception{
        this.LC = 0;
        for(String line : this.code){
            line = line.strip().toUpperCase();
            int labeldiv = line.indexOf(",");
            if(labeldiv!=-1){
                line = line.substring(labeldiv+1, line.length()).strip();
            }
            String instruction = "HLT";
            String address = "";
            String[] lineDiv = line.split(" ");
            boolean isI = false;
            switch(lineDiv.length){
                default:
                case 3: if(lineDiv[2].equals("I")){isI=true;}
                case 2: address = lineDiv[1];
                case 1: instruction = lineDiv[0];
            }
            switch(Arrays.asList(this.Pseudo).indexOf(instruction)){
                case 0:this.LC = Integer.parseInt(address); break;
                case 1:return;
                case 2:this.addMLC(Integer.parseInt(address)); this.LC++;break;
                case 3:this.addMLC(Integer.parseInt(address, 16)); this.LC++;break;
                case -1:
                    int code = 0;
                    int instructionIndex = Arrays.asList(this.MRI).indexOf(instruction);
                    if(instructionIndex!=-1){
                        code |= instructionIndex<<12;
                        for(Hash hash : this.SymbolTable){
                            if(hash.getKey().equals(address)){
                                code|=hash.getValue();
                                break;
                            }
                        }
                        if(isI){code|=0x8000;}
                        this.addMLC(code);
                        this.LC++;
                    }
                    else{
                        instructionIndex = Arrays.asList(this.RRI).indexOf(instruction);
                        if(instructionIndex!=-1){code|=0x7000; code|=1<<(11-instructionIndex);}
                        else{
                            instructionIndex = Arrays.asList(this.IOI).indexOf(instruction);
                            if(instructionIndex!=-1){code|=0xF000;code|=1<<(11-instructionIndex);}
                            else{throw new Exception("Invalid Instruction Detected!");}
                        }
                        this.addMLC(code);
                        this.LC++;
                    }

            }
        }
        return;
    }

    private void saveOutputFile() throws IOException{
        //System.out.println(String.format("\n\n\nMachine Language Code :\n%s", this.MLC));
        File outputFile = new File(this.outputFilename);
        if(!outputFile.exists()){
            outputFile.createNewFile();
        }
        PrintWriter printer = new PrintWriter(new FileWriter(outputFile));
        
        printer.print(this.MLC);
        printer.close();
        
        return;
    }


    public static void main(String[] args) {
        //System.out.println(String.format("%s | %s", args[0], args[1]));
        Jade asm = new Jade(args);
        asm.compile();
        return;
    }
}