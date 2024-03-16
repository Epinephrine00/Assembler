package jasm;

public class Jade {
    public String getGreeting() {
        return "Hello World!";
    }

    public static void main(String[] args) {
        System.out.println(new Jade().getGreeting());
    }
}
