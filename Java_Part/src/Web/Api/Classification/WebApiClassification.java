package Web.Api.Classification;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.logging.Level;
import java.util.logging.Logger;

public class WebApiClassification {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) 
    {
        
        
        WebApiClassification a3=new WebApiClassification();

        a3.read_api_file();
       
      
        
        
        
    }
    
    public void read_api_file()
    {
        /*
        Reads the api file and loads into the database
        
        */
        //MongoClient mongo = new MongoClient( "localhost" , 27017); //connect to mongo
        //MongoDatabase db=mongo.getDatabase("mydb"); //access database
        //db.createCollection("api"); //create collection(table name) if not present
        //MongoCollection<Document> collection = db.getCollection("api"); //access collection
 
        try 
        {

            File f = new File("/Users/parthamehta/Desktop/api.txt");

            BufferedReader b = new BufferedReader(new FileReader(f));

            String readLine = "";
          
            String[] api_col={"id","title","summary","rating","name","label","author","description",
                "type","downloads","useCount","sampleUrl","downloadedUrl","dateModified","remoteFeed","numComments",
            "commentsUrl","Tags","category","protocols","serviceEndpoint","version","wsdl",
            "data formats","apigroups","example","clientInstall","authentication","ssl","readonly","VendorApiKits","CommunityAPIKits",
            "blog","forum","support","accountReq","commercial","provider","managedBy","nonCommercial","dataLicensing",
            "fees","limits","terms","company","updated"};
            
            System.out.println("Reading file using Buffered Reader");
            ArrayList<String> description=new ArrayList<String>();
            ArrayList<String> category=new ArrayList<String>();
            
            HashSet<String> hset=new HashSet<String>();
            
            while ((readLine = b.readLine()) != null) 
            {
              
              String[] output = readLine.split("\\$\\#\\$");
              //Document d=new Document("count",count);
              String summary="";
               for(int i=0;i<output.length;i++)
               {
                   output[i]=output[i].trim();
                   if(output[i].length()==0 || output[i].isEmpty())
                       output[i]="null";
                   else if(output[i].contains("###"))
                   {
                       String replace=output[i].replace("###", ";");
                       output[i]=replace;
                       
                   }
                   
                   //System.out.print(output[i]+" ");
                   if(api_col[i].equals("summary"))
                   {
                      summary+=output[i]; 
                   }
                   
                   if(api_col[i].equals("description"))
                   {
                       output[i]+=summary;
                       if(output[i].contains(","))
                       {
                          String replace=output[i].replace(",", " ");
                          output[i]=replace;
                      }
                       
                      if(output[i].contains(";"))
                       {
                          String replace=output[i].replace(";", " ");
                          output[i]=replace;
                        }
                       description.add(output[i]);
                       
                       
                   }
                   
                   if(api_col[i].equals("category"))
                  {
                       
                      if(output[i].contains(","))
                      {
                           String replace=output[i].replace(",", " ");
                          output[i]=replace;
                      }
                       
                      if(output[i].contains(";"))
                      {
                         String replace=output[i].replace(";", " ");
                          output[i]=replace;
                        }
                       category.add(output[i]);
                       hset.add(output[i]);
                   }
                   
                   
                   //d.append(api_col[i], output[i]);
                   
               }
               
               //System.out.println();
               
               //collection.insertOne(d);  //insert into table
               
            }
            
            System.out.println(description.size());
            System.out.println(category.size());
            System.out.println(hset);
            System.out.println(hset.size());
            write_csv(description,category);
            
            

        } catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
    
    public void write_csv(ArrayList<String> description, ArrayList<String> category)
    {
        String file_header = "description,category";
        String new_line_separator = "\n";
        String comma_delimiter = ",";


        FileWriter fileWriter = null;
        try 
        {
            fileWriter = new FileWriter("/Users/parthamehta/Desktop/api_csv.csv");
            fileWriter.append(file_header);
            fileWriter.append(new_line_separator);
            
            for(int i=0;i<description.size();i++)
            {
                fileWriter.append(description.get(i));
                fileWriter.append(comma_delimiter);
                fileWriter.append(category.get(i));
                fileWriter.append(new_line_separator);
                
            }
            
            fileWriter.close();


        } 
        
        catch (IOException ex) 
        {
            Logger.getLogger(WebApiClassification.class.getName()).log(Level.SEVERE, null, ex);
        }
        

        

        

    }
    
    
    
       
}

