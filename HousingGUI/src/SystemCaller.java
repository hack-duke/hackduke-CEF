public class SystemCaller {

	public SystemCaller(){
		
	}
	
	public void call(String city, String state, String limit){
        try {
        	String[] cmd = {"/Users/Gideon/bash_scripts/generatehousing.sh",
        			"city=" + city, "state=" + state, "limit=" + limit};
            Runtime rt = Runtime.getRuntime();
            Process proc = rt.exec(cmd);
//            proc.waitFor();
        	} catch (Throwable t) {
        		t.printStackTrace();
        	}
	}
}
