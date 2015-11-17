package lucene;


import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.util.*;
import java.io.IOException;
import java.util.Iterator;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class IndexFiles {
	
	public double GetPoint(Double[] arr) {
		int point = arr[0]
		
	}
	public static void main(String[] args) {
		
		JSONParser parser = new JSONParser();
		InputStream is = null;
		InputStreamReader isr = null;
		BufferedReader br = null;
		
		try {
			is = new FileInputStream("/Users/admin/Documents/workspace/Twitter-Search-Engine/data/raw_tweets1_visited.json");
			isr = new InputStreamReader(is);
			br = new BufferedReader(isr);
			String line;
			
			while((line = br.readLine()) != null)
			{
				Object obj = parser.parse(line);
				JSONObject jsonObject = (JSONObject) obj;
				
				String name = (String) jsonObject.get("name");
				System.out.println("name: " + name);
				
				String title = (String) jsonObject.get("title");
				System.out.println("title:" + title);
				String text = (String) jsonObject.get("text");
				System.out.println("text: "+ text);
				// loop array
				JSONArray hashtags = (JSONArray) jsonObject.get("htags");
				for (int i=0; i < hashtags.size(); ++i){
					JSONObject hobj = (JSONObject) hashtags.get(i);
					String htext = (String) hobj.get("text");
					System.out.println("hashtag: " + htext);
				}
				JSONArray loc = (JSONArray) jsonObject.get("location");
				JSONArray lo = (JSONArray) loc.get(0);
				JSONArray l = (JSONArray) lo.get(0);
				for(int i = 0; i < l.size(); ++i) {
					System.out.println(l.get(i));
				}
				
			}
		} catch (FileNotFoundException e) {
				e.printStackTrace();
		} catch (IOException e) {
				e.printStackTrace();
		} catch (ParseException e) {
				e.printStackTrace();
		}

	}	
}
