
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class main extends Application {
	private GridPane gridpane;
	private Stage primaryStage;
	private String city, state, limit;
	private SystemCaller caller;
	
    public static void main(String[] args) {
        launch(args);
    }
    
    private void makeGridPane(){
    	
    	//Creating a GridPane container
    	GridPane grid = gridpane;
    	grid.setPadding(new Insets(10, 10, 10, 10));
    	grid.setVgap(5);
    	grid.setHgap(5);
    	
    	//Defining the Name text field
    	final TextField name = new TextField();
    	name.setPromptText("Enter the city ex. (Newark)");
    	name.setPrefColumnCount(10);
    	name.getText();
    	GridPane.setConstraints(name, 0, 0);
    	grid.getChildren().add(name);
    	
    	//Defining the Last Name text field
    	final TextField lastName = new TextField();
    	lastName.setPromptText("Enter the state abbrev ex. (NJ)");
    	GridPane.setConstraints(lastName, 0, 1);
    	grid.getChildren().add(lastName);
    	
    	//Defining the Comment text field
    	final TextField comment = new TextField();
    	comment.setPrefColumnCount(15);
    	comment.setPromptText("Enter max price limit");
    	GridPane.setConstraints(comment, 0, 2);
    	grid.getChildren().add(comment);
    	
    	//Defining the Submit button
    	Button submit = new Button("Submit");
    	GridPane.setConstraints(submit, 1, 0);
    	grid.getChildren().add(submit);
    	
    	//Defining the Clear button
    	Button clear = new Button("Clear");
    	GridPane.setConstraints(clear, 1, 1);
    	grid.getChildren().add(clear);
    	
    	//Adding a Label
    	final Label label = new Label();
    	GridPane.setConstraints(label, 0, 3);
    	GridPane.setColumnSpan(label, 2);
    	grid.getChildren().add(label);
    	
    	//Setting an action for the Submit button
    	submit.setOnAction(new EventHandler<ActionEvent>() {

    	@Override
    	    public void handle(ActionEvent e) {
    	        if ((comment.getText() != null && !comment.getText().isEmpty()) &&
    	        		name.getText() != null && !name.getText().isEmpty() && 
    	        		lastName.getText() != null && !lastName.getText().isEmpty()) {
    	            label.setText("Please close this application");
    	            caller.call(name.getText(), lastName.getText(), comment.getText());
    	            primaryStage.close();
    	        } else {
    	            label.setText("You have not entered all information");
    	        }
    	     }
    	 });
    	
    	//Setting an action for the Clear button
    	clear.setOnAction(new EventHandler<ActionEvent>() {

    	@Override
    	    public void handle(ActionEvent e) {
    	        name.clear();
    	        lastName.clear();
    	        comment.clear();
    	    }
    	});
    }
    
    public void initialize(Stage primaryStage){
    	this.caller = new SystemCaller();
    	this.gridpane = new GridPane();
    	this.primaryStage = primaryStage;
        this.primaryStage.setTitle("Housing Generator");
        this.primaryStage.setScene(new Scene(this.gridpane, 300, 130));
        this.primaryStage.show();
    }
    
    @Override
    public void start(Stage primaryStage) {
    	initialize(primaryStage);
    	makeGridPane();
      
    }
}