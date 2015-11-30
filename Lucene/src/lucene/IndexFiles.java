package lucene;


import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.FileInputStream;
import java.util.*;
import java.io.IOException;
import java.util.Iterator;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.io.File;

import java.util.StringTokenizer;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.DoubleField;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.CorruptIndexException;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
//import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

class Tweet {
	public String name;
	public String title;
	public String text;
	public String [] htags;
	public double [] location;
	public String created_at;
	
	public Tweet(String n, String tit, String tex, JSONArray ht, double []loc, String c) {
		this.name = n;
		this.title = tit;
		this.text = tex;
		this.htags = new String[ht.size()];
		
		for(int i = 0; i < ht.size(); i++) {
			JSONObject hobj = (JSONObject) ht.get(i);
			this.htags[i] = (String) hobj.get("text");
		}
		this.location = new double[2];
		for(int i = 0; i < loc.length; i++) {
			this.location[i] = loc[i];
		}
		this.created_at = c;
	}
}


public class IndexFiles {
	
	
	
	public static void main(String[] args) {

	 	try {
	 		File folder = new File("/Users/admin/Documents/workspace/Twitter-Search-Engine/data");
	 		File[] listOfFiles = folder.listFiles();
	 		
	 		for (int i = 0; i < listOfFiles.length; ++i) {
	 			System.out.println(i);

	 			System.out.println(listOfFiles[i].getName());
	 	
			   	InputStream is = new FileInputStream("/Users/admin/Documents/workspace/Twitter-Search-Engine/data/" + listOfFiles[i].getName());
			   	InputStreamReader isr = new InputStreamReader(is);
			   	BufferedReader br = new BufferedReader(isr);
				String line;
				StandardAnalyzer analyzer = new StandardAnalyzer();
				Path path = Paths.get("/Users/admin/Documents/workspace/Twitter-Search-Engine/index");
				Directory dir = FSDirectory.open(path);
				IndexWriterConfig config = new IndexWriterConfig(analyzer);
			    IndexWriter iwriter = new IndexWriter(dir, config);
				while((line = br.readLine()) != null)
				{
				 	JSONParser parser = new JSONParser();
					Object obj = parser.parse(line.toString());
					JSONObject jsonObject = (JSONObject) obj;
					
					String name = (String) jsonObject.get("name");
					String title = (String) jsonObject.get("title");
					String text = (String) jsonObject.get("text");
					String created = (String) jsonObject.get("created_at");
					JSONArray hashtags = (JSONArray) jsonObject.get("htags");
					JSONArray reducedLoc = (JSONArray) jsonObject.get("location");
					JSONArray locArray = (JSONArray) reducedLoc.get(0);
					double []loc = new double[2];
					loc = GetPoint(locArray);
					
					Tweet tweet = new Tweet(name, title, text, hashtags, loc, created);
					index(tweet,iwriter);
					
					
				}
				br.close();
				is.close();
				isr.close();
			    iwriter.close();	
		    
	 		}
		} catch (FileNotFoundException e) {
			  	e.printStackTrace();
		} catch (IOException e) {
		  		e.printStackTrace();
		} catch (ParseException e) {
		  		e.printStackTrace();
		}
	
	}
	
	public static void index(Tweet tweet, IndexWriter iwriter) {
		try{
		    Document doc = new Document();
		    //int day = Integer.parseInt(tweet.created_at.substring(8, 10));
			//float score = (float) Math.abs((11.0 - day) * 0.3) + 1;
			
		    doc.add(new Field("name", tweet.name, TextField.TYPE_STORED));
		    doc.add(new Field("tweet", tweet.text, TextField.TYPE_STORED ));
		    
		    doc.add(new Field("created_at", tweet.created_at, TextField.TYPE_STORED ));
		    if (tweet.title != null){
			    doc.add(new Field("title", tweet.title, TextField.TYPE_STORED ));
		    }else {
		    	doc.add(new Field("title", "null", TextField.TYPE_STORED ));
		    }
		    
		    if (tweet.htags.length > 0) {
		    	String tags = "";
			    for (int i = 0; i < tweet.htags.length; i++){
			    	tags = tags.concat(tweet.htags[i] + " ");
			    }
			    tags = tags.substring(0, tags.length() - 1);	//remove last space character
			    doc.add(new Field("htag", tags, TextField.TYPE_STORED ));
		    }
		    else {
		    	doc.add(new Field("htag", "null", TextField.TYPE_STORED ));
		    }
		    doc.add(new DoubleField("longitude", tweet.location[0], DoubleField.TYPE_STORED));
		    doc.add(new DoubleField("latitude", tweet.location[1], DoubleField.TYPE_STORED));
		    
		    iwriter.addDocument(doc);

		} catch (Exception ex){
		  	ex.printStackTrace();;
		}
	}
	
	public static double[] GetPoint(JSONArray arr) {
		JSONArray first = (JSONArray) arr.get(0);
		JSONArray second = (JSONArray) arr.get(1);
		JSONArray third = (JSONArray) arr.get(2);
		double ay = (double) first.get(1);
		double bx = (double) second.get(0);
		double by = (double) second.get(1);
		double cx = (double) third.get(0);
		double []location = new double[2];
		double lon = (bx + cx)/2.0;
		double lat = (ay + by)/2.0;
		location[0] = lon;
		location[1] = lat;
		return location;
	}
}

