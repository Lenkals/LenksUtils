import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class CSVReaderCoreJava {
    public static void main(String[] args) {
        String filePath = "D:\\Dev\\stocks\\EQUITY_L.csv"; // Replace with your CSV file path
        CSVReaderCoreJava foo = new CSVReaderCoreJava();
        List <String[]>  nse=foo.getFileInfo("D:\\Dev\\stocks\\EQUITY_L.csv",1);
        List <String[]> grow= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl-groww.csv",10);
        List <String[]> zero= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl_0dha.csv",10);
        List <String[]> a1= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl_a1.csv",10);
        List <String[]> mstock= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl_gmstock.csv",10);
        List <String[]>  finalList=new ArrayList<>();
        List <String[]>  growList=getIsinSymbol(nse,grow);
        List <String[]>  zeroList=getIsinSymbol(nse,zero);
        List <String[]>  a1List=getIsinSymbol(nse,a1);
        List <String[]>  mstockList=getIsinSymbol(nse,mstock);

        finalList.addAll(growList);
        finalList.addAll(mstockList);
        finalList.addAll(zeroList);
        finalList.addAll(a1List);

        for(String[] line:finalList){
            System.out.print("Isin:"+line[0]);
            System.out.println(" Symbol:"+line[1]);
        }
    //    Map<String,String[]>  zerodha= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl_0dha.csv",10,1);
      //  Map<String,String[]>  a1= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl_a1.csv",10,1);
     //   Map<String,String[]>  mstock= foo.getFileInfo("D:\\Dev\\stocks\\BO_Details_Cdsl_mstock.csv",10,1);
    
            }
    

    public List <String[]> getFileInfo(String filePath,int readLineFrom){
        List<String[]> list=new ArrayList<>();
        int count=0;
        String line;
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            while ((line = br.readLine()) != null) {
                count++;
                if(count<readLineFrom){ continue;}
                // Split by comma
                String[] values = line.split(",");
                list.add(values);
                
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
         System.out.println("size of map "+filePath+"  -->"+list.size());
        return list;
    }

    public static List <String[]>  getIsinSymbol(List <String[]> nse,List <String[]> brokeList){
        List <String[]> list=new ArrayList<>();
        for(String[] line:brokeList){
            String isin=line[1].replace("\"", "");
            for(String[] line2:nse){
                if(isin.equalsIgnoreCase(line2[6])){
                    String[] arr=new String[2];
                    arr[0]=isin;
                    arr[1]=line2[0];
                  //  System.out.println("isin :: "+isin+" Symbol ::"+line2[0]);  
                    list.add(arr);
                    break;
                }else{
                   // System.out.println("isin :: "+isin+" isin in nse ::"+line2[6]); 
                }

            }
    }
        return list;

    }
}
