<%@ 
page import="java.nio.file.Path"
import = "java.nio.file.Paths"
import = "java.util.HashMap"
import ="java.util.Map"
import ="org.apache.lucene.analysis.standard.StandardAnalyzer"
import ="org.apache.lucene.document.Document"
import ="org.apache.lucene.index.DirectoryReader"
import ="org.apache.lucene.search.IndexSearcher"
import ="org.apache.lucene.search.Query"
import ="org.apache.lucene.queryparser.classic.MultiFieldQueryParser"
import ="org.apache.lucene.search.ScoreDoc"
import= "org.apache.lucene.store.Directory"
import= "org.apache.lucene.store.FSDirectory"
%> 
<head>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
</head>


<body>
	<nav class="navbar navbar-default">
	  <div class="container-fluid">
	  
	    <div class="navbar-header">
	      <a class="navbar-brand" href="#">Skywalker Search</a>
	    </div>
	    
	  </div>
	</nav>
	<div class="container">
	
   		<form role="search" action="index.jsp" method="POST">
	       <div class="input-group input-group-lg col-md-6 col-md-offset-3">
			  <span class="input-group-addon" id="sizing-addon2"><span class="glyphicon glyphicon-search"></span></span>
			  <input type="text" class="form-control" placeholder="Search" aria-describedby="sizing-addon2" name="query">
			</div>
	    </form>
	    	    
		<% 
			try{
				Path path = Paths.get("/Users/admin/Documents/workspace/Twitter-Search-Engine/index");
				Directory dir = FSDirectory.open(path);
				DirectoryReader ireader = DirectoryReader.open(dir);
				IndexSearcher isearcher = new IndexSearcher(ireader);
				StandardAnalyzer analyzer = new StandardAnalyzer();
				//get each token
				Map<String, Float> boosts = new HashMap<String, Float>();
				boosts.put("tweet", 4.0f);
				boosts.put("title", 1.5f);
				boosts.put("htag", 2.0f);
				MultiFieldQueryParser parser = new MultiFieldQueryParser(new String[] {"tweet", "title", "htag"}, analyzer, boosts);
				Query query = parser.parse(request.getParameter("query"));
				
				ScoreDoc[] hits = isearcher.search(query, null, 200).scoreDocs;
				
					for (int i = 0; i <  hits.length; i++){
				%><div class="well">
					<pre><% 
						Document hitDoc = isearcher.doc(hits[i].doc);
						out.println("Tweet: " + hitDoc.get("tweet") + "\n");
						out.print("By: " + hitDoc.get("name"));
						if (! hitDoc.get("title").equals("null")){
							out.print("\ttitle: " + hitDoc.get("title"));
						}
						out.println();
						out.print("created at: " + hitDoc.get("created_at"));
						%>
					</pre></div>
					<%
					} 
				
				

				
				
			} catch(Exception e){
				e.printStackTrace();
			}
		%> 
	    
	</div>
</body>


