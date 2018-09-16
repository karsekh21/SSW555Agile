import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Gedcom 
{
	public static void main(String[] args) throws IOException
	{
		System.out.print("Please enter your file name:");
		Scanner in=new Scanner(System.in);
		String input=in.nextLine();
		File file=new File(input);
		
		Map<String, String> map=new HashMap<String, String>();
		
		map.put("INDI", "0");
		map.put("NAME", "1");
		map.put("SEX", "1");
		map.put("BIRT", "1");
		map.put("DEAT", "1");
		map.put("FAMC", "1");
		map.put("FAMS", "1");
		map.put("FAM", "0");
		map.put("MARR", "1");
		map.put("HUSB", "1");
		map.put("WIFE", "1");
		map.put("CHIL", "1");
		map.put("DIV", "1");
		map.put("DATE", "2");
		map.put("HEAD", "0");
		map.put("TRLR", "0");
		map.put("NOTE", "0");
		
		try(BufferedReader br=new BufferedReader(new FileReader(file)))
		{
			String line;
			while((line=br.readLine())!=null)
			{

				System.out.println("--> "+line);
				
				String[] split=line.split(" ");
				
				//if(map.get(split[2]).equals(split[0]))
				if(map.containsKey(split[1]) && map.get(split[1]).equals(split[0]) && !(split[1].equals("INDI")) && !(split[1].equals("FAM")))
				{
					System.out.print("<-- "+split[0]+"|"+split[1]+"|"+"Y"+"|");
					for(int i=2; i<split.length; i++)
					{
						System.out.print(split[i]);
						
						if(i!=split.length-1)
							System.out.print(" ");

					}
				}
				else if(split.length<3)
					System.out.print("<-- "+split[0]+"|"+split[1]+"|"+"N"+"|");
				else if(map.containsKey(split[2]) && map.get(split[2]).equals(split[0]))
					System.out.print("<-- "+split[0]+"|"+split[2]+"|"+"Y"+"|"+split[1]);
				else if(split[2].equals("INDI") || split[2].equals("FAM"))
					System.out.print("<-- "+split[0]+"|"+split[2]+"|"+"N"+"|"+split[1]);
				else
				{
					System.out.print("<-- "+split[0]+"|"+split[1]+"|"+"N"+"|");
					for(int i=2; i<split.length; i++)
					{
						System.out.print(split[i]);
						
						if(i!=split.length-1)
							System.out.print(" ");

					}
				}
				

				System.out.println("");

				
			}
		}
		in.close();
		
		return;
		
		
	}
	
}
