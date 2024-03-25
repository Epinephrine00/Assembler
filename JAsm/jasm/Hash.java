package jasm;

public class Hash{
    private String key;
    private int value;
    public Hash(String key, int value){
        this.key = key;
        this.value = value;
    }
    public String getKey(){return this.key;}
    public int getValue(){return this.value;}
}