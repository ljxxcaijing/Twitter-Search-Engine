package lucene;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;


import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.queryparser.classic.MultiFieldQueryParser;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class SearchFiles {
	
	public static void main(String[] args){
		try{
			
			Path path = Paths.get("/Users/admin/Documents/workspace/Twitter-Search-Engine/index");
			Directory dir = FSDirectory.open(path);
			DirectoryReader ireader = DirectoryReader.open(dir);
			IndexSearcher isearcher = new IndexSearcher(ireader);
			StandardAnalyzer analyzer = new StandardAnalyzer();
			//get each token
			Map<String, Float> boosts = new HashMap<String, Float>();
			boosts.put("tweet", 4.0f);
			boosts.put("title", 2.0f);
			boosts.put("htag", 6.0f);
			MultiFieldQueryParser parser = new MultiFieldQueryParser(new String[] {"tweet", "title", "htag"}, analyzer, boosts);
			Query query = parser.parse("corey");
			ScoreDoc[] hits = isearcher.search(query, null, 20).scoreDocs;
			for (int i = 0; i <  hits.length; i++){
				Document hitDoc = isearcher.doc(hits[i].doc);
				System.out.println("Tweet: " + hitDoc.get("tweet"));
				System.out.println("Hash: " + hitDoc.get("htag"));
				System.out.println("title: " + hitDoc.get("title"));
				System.out.println("created_at: " + hitDoc.get("created_at"));
				System.out.println();
				System.out.println();

			}
			
			
		} catch(Exception e){
			e.printStackTrace();
		}
	}
}