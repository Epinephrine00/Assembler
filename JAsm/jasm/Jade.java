// JADE.java
// Java-Assembler Developed by Epinephrine00
// java jasm/Jade "Path_of_Your_ASM_File.asm"
// java jasm/Jade "Path_of_Your_ASM_File.asm" "Path_of_Output_OBJE_File.obje"
// Recommended Output File Extension : *.obje (OBJect defined by Epinephrine00)


package jasm;

import java.util.ArrayList;
import java.io.File;
import java.io.IOException;
import java.util.Scanner;
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
    private String            MLC;

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
            //System.out.println(this.code.get(1));
        }
        else{
            return;
        }
    }

    public void compile(){
        this.firstPass();
        this.secondPass();
        try{this.saveOutputFile();}
        catch(IOException e){System.out.println(e.toString());return;}
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
            System.out.println(String.format("line = %s : instruction : %s | address : %s", line, instruction, address));
            if(line.indexOf(",")!=-1){
                String label = line.substring(0,line.indexOf(","));
                System.out.println(String.format("Labeled! label : %s", label));
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
                //for(Hash hash : this.SymbolTable){System.out.println(String.format("hash key : %s | value : %d", hash.getKey(), hash.getValue()));}
                return;
            }
            else{
                this.LC++;
            }
        }
        
        return;
    }

    private void secondPass(){
        this.LC = 0;
        for(String line : this.code){
            line = line.strip().toUpperCase();
        }
        return;
    }

    private void saveOutputFile() throws IOException{
        return;
    }

    public static void main(String[] args) {
        //System.out.println(String.format("%s | %s", args[0], args[1]));
        Jade asm = new Jade(args);
        asm.compile();
        return;
    }
}