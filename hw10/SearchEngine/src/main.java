
import java.util.Scanner;

public class main {
    public static void main(String []args) {
        SearchEngine createIndex = new SearchEngine();
        Scanner in = new Scanner(System.in);
        while(true) {
            System.out.print("输入文字以查询（输入q退出）：");
            String text = in.nextLine();
            if(text.equals("q")){
                break;
            }
            createIndex.search(text);
        }
    }
}
