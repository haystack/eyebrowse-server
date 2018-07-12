package recommender;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.grouplens.lenskit.data.sql.JDBCRatingDAO;
import org.grouplens.lenskit.transform.normalize.BaselineSubtractingUserVectorNormalizer;
import org.grouplens.lenskit.transform.normalize.UserVectorNormalizer;
import org.lenskit.LenskitConfiguration;
import org.lenskit.LenskitRecommender;
import org.lenskit.api.ItemScorer;
import org.lenskit.api.RatingPredictor;
import org.lenskit.baseline.BaselineScorer;
import org.lenskit.baseline.ItemMeanRatingItemScorer;
import org.lenskit.baseline.UserMeanBaseline;
import org.lenskit.baseline.UserMeanItemScorer;
import org.lenskit.basic.SimpleRatingPredictor;
import org.lenskit.knn.item.ItemItemScorer;

import it.unimi.dsi.fastutil.longs.LongSet;

public class WebPageRecommender implements Runnable {


    public static void main(String[] args) {
       WebPageRecommender recommender = new WebPageRecommender(args);
        try {
            recommender.run();
        } catch (RuntimeException e) {
            System.err.println(e.toString());
            e.printStackTrace(System.err);
            System.exit(1);
        }
    }
	private List<String> users;

    public WebPageRecommender(String[] args) {
    	this.users = new ArrayList<String>();
    	for (String arg: args) {
    		this.users.add(arg);
    	}
    }
    
    
    
    private LenskitConfiguration configure() {
        // We first need to configure the data access.
        // We will load data from a static data source; you could implement your own DAO
        // on top of a database of some kind
    	LenskitConfiguration config = new LenskitConfiguration();
		// Use item-item CF to score items
		config.bind(ItemScorer.class)
		      .to(ItemItemScorer.class);
		// Use item scorer to calculate item ratings
		config.bind(RatingPredictor.class)
			  .to(SimpleRatingPredictor.class);
		// let's use personalized mean rating as the baseline/fallback predictor.
		// 2-step process:
		// First, use the user mean rating as the baseline scorer
		config.bind(BaselineScorer.class, ItemScorer.class)
		      .to(UserMeanItemScorer.class);
		// Second, use the item mean rating as the base for user means
		config.bind(UserMeanBaseline.class, ItemScorer.class)
		      .to(ItemMeanRatingItemScorer.class);
		// and normalize ratings by baseline prior to computing similarities
		config.bind(UserVectorNormalizer.class)
		      .to(BaselineSubtractingUserVectorNormalizer.class);  
		return config;
    }
    
    private Connection getConnection() throws SQLException {
        Connection conn = null;
        Properties connectionProps = new Properties();
        connectionProps.put("user", "admin");
        connectionProps.put("password", "ROLO#27!");
        conn = DriverManager.getConnection(
                       "jdbc:" + "mysql" + "://" +
                       "localhost" +
                       ":" + "3306" + "/",
                       connectionProps);  
        System.out.println("Connected to database");
        return conn;
    }
    
    
    public void run() {	
		Connection cxn;
		try {
			cxn = this.getConnection();
		} catch (SQLException e) {
			e.printStackTrace();
			return;
		}
		
		JDBCRatingDAO dao = JDBCRatingDAO.newBuilder().setTableName("api_ratings").build(cxn);
	    LenskitConfiguration config = this.configure();
	    config.addComponent(dao);
	    
	    LenskitRecommender rec = LenskitRecommender.build(config);
	    RatingPredictor rp = rec.getRatingPredictor();
	    LongSet items = dao.getItemIds();
	    
        for (String user : users) {
        	Long uid = Long.parseLong(user);
        	HashMap<Long, Double> item_scores = (HashMap<Long, Double>) rp.predict(uid, items);
        
            System.out.format("Recommendations for user %d:\n", user);
            
            for (Map.Entry<Long, Double> item : item_scores.entrySet()) {
                System.out.format("\t%d : %.2f\n", item.getKey(), item.getValue());
            }
        }
        rec.close();
	}
}