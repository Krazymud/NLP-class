
import org.apache.commons.io.FileUtils;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.cn.smart.SmartChineseAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StoredField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.highlight.*;
import org.apache.lucene.search.spell.LuceneDictionary;
import org.apache.lucene.search.spell.PlainTextDictionary;
import org.apache.lucene.search.spell.SpellChecker;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;


import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.nio.file.Paths;

public class SearchEngine {
    public static final String DATA_DIR = "C:\\Users\\Eadric\\Desktop\\hw10\\SearchEngine\\data\\page";
    public static final String INDEX_DIR = "C:\\Users\\Eadric\\Desktop\\hw10\\SearchEngine\\index";
    public static final String SINDEX_DIR = "C:\\Users\\Eadric\\Desktop\\hw10\\SearchEngine\\spellindex";

    public void createIndex(){
        try{
            Directory dir = FSDirectory.open(Paths.get(INDEX_DIR));
            Analyzer analyzer = new SmartChineseAnalyzer();
            IndexWriterConfig config = new IndexWriterConfig(analyzer);
            IndexWriter indexWriter = new IndexWriter(dir, config);
            File files = new File(DATA_DIR);
            for(File f : files.listFiles()){
                String fileName = f.getName();
                String fileContent = FileUtils.readFileToString(f, "utf-8");
                String filePath = f.getPath();
                long fileSize = FileUtils.sizeOf(f);

                Document document = new Document();
                Field nameField = new TextField("name", fileName, Field.Store.YES);
                Field contentField = new TextField("content", fileContent, Field.Store.YES);
                Field pathField = new StoredField("path", filePath);
                Field sizeField = new StoredField("size", fileSize);
                document.add(nameField);
                document.add(contentField);
                document.add(pathField);
                document.add(sizeField);
                indexWriter.addDocument(document);
            }
            indexWriter.close();
        } catch(Exception e){
            e.printStackTrace();
        }
    }
    public void search(String text){
        try{
            SmartChineseAnalyzer analyzer=new SmartChineseAnalyzer();

            Directory dir = FSDirectory.open(Paths.get(INDEX_DIR));
            SpellChecker spellChecker = new SpellChecker(dir);
            IndexReader indexReader = DirectoryReader.open(dir);
            spellChecker.indexDictionary(new LuceneDictionary(indexReader, "content"), new IndexWriterConfig(analyzer), false);
            IndexSearcher indexSearcher = new IndexSearcher(indexReader);
            TermQuery query = new TermQuery(new Term("content", text));

            long start = System.currentTimeMillis();
            TopDocs topDocs = indexSearcher.search(query, 5);
            long end = System.currentTimeMillis();

            System.out.println("匹配 " + text + " ,总共花费了" + (end-start) +"毫秒,共查到" + topDocs.totalHits + "条记录。");
            if(topDocs.totalHits.value == 0){
                String[] suggestions = spellChecker.suggestSimilar(text, 5);
                if(suggestions.length > 0){
                    System.out.println("你要找的是 " + suggestions[0] + " 吗？");
                }
            }
            else{
                System.out.println("评分前五的结果：");

                ScoreDoc[] scoreDocs = topDocs.scoreDocs;
                QueryScorer scorer = new QueryScorer(query);
                Fragmenter fragmenter = new SimpleSpanFragmenter(scorer);
                SimpleHTMLFormatter simpleHTMLFormatter = new SimpleHTMLFormatter();
                Highlighter highlighter = new Highlighter(simpleHTMLFormatter, scorer);
                highlighter.setTextFragmenter(fragmenter);

                for(ScoreDoc scoreDoc : scoreDocs){
                    int docID = scoreDoc.doc;
                    float score = scoreDoc.score;
                    Document document = indexSearcher.doc(docID);
                    System.out.println(document.get("name") + " 相关度得分：" + score);
                    String content = document.get("content");
                    if(content!=null){
                        //第一个参数是对哪个参数进行设置；第二个是以流的方式读入
                        TokenStream tokenStream = analyzer.tokenStream("content", new StringReader(content));
                        //获取最高的片段
                        System.out.println(highlighter.getBestFragment(tokenStream, content));
                    }
                }
            }
            System.out.println();
            indexReader.close();
        } catch(Exception e){
            e.printStackTrace();
        }

    }
}
