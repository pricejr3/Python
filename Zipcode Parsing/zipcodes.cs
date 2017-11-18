using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Collections.Specialized;


	public class zipcodes {

	public static List<String> citiesList = new List<String>();
	public static List<String> zipsList = new List<String>();
	public static List<String> statesList = new List<String>();
	public static List<String> commonCityNames = new List<String>();
	public static List<String> latitude = new List<String>();

	public static NameValueCollection nvc = new NameValueCollection();
	public static NameValueCollection commonCity = new NameValueCollection();


	
    public static void populateLists()
    {
        StreamReader input = new StreamReader("cities.txt");
        while (!input.EndOfStream)
        {
            string line = input.ReadLine();
            string[] toks = line.Split('\t');

            foreach (string value in toks)
            {
                citiesList.Add(value);
            }


        }

        input.Close();


        input = new StreamReader("zips.txt");
        while (!input.EndOfStream)
        {
            string line = input.ReadLine();
            string[] toks = line.Split('\t');

            foreach (string value in toks)
            {


                zipsList.Add(value);
            }


        }

        input.Close();


        input = new StreamReader("states.txt");
        while (!input.EndOfStream)
        {
            string line = input.ReadLine();
            string[] toks = line.Split('\t');

            foreach (string value in toks)
            {


                statesList.Add(value);
            }


        }

        input.Close();
    }

	


    public static void CommonCityNames(){


            List<String> printList = new List<String>();
	    List<String> finalList = new List<String>();
	    bool populatedFinalList = false;
		StreamWriter output = new StreamWriter("CommonCityNames.txt");
	 	
	

		StreamReader input = new StreamReader("zipcodes.txt");
			
			while (!input.EndOfStream) {
				string line = input.ReadLine();
				string[] toks = line.Split('\t');
				if(statesList.Contains(toks[4])){
				
					nvc.Add(toks[4], toks[3]);

				}
				
			}
	   string[] values = null;


	  
           foreach (string key in statesList) {


		// Clear the printList
		printList.Clear();
		

                values = nvc.GetValues(key);

                foreach (string value in values)
                {
                      printList.Add(value);

                } 

		if(populatedFinalList == false){

			finalList = printList;

			populatedFinalList = true;
		}

		
		List<String> tmpList = new List<String>();
		tmpList = printList.Intersect(finalList).ToList();

		finalList = tmpList;


	
	} // end iteration
	  
		finalList.Sort();
		foreach (string value in finalList){
                    
		  output.Write(value);
		  output.Write("\n");

               } // end foreach
 	
	    
		

   
		output.Close();
} 


    public static void LatLon(){

		StreamReader input = new StreamReader("zipcodes.txt");
			
			while (!input.EndOfStream) {
				string line = input.ReadLine();
				string[] toks = line.Split('\t');
				
				if(zipsList.Contains(toks[1])){
					
					latitude.Add(toks[6]);
					latitude.Add(toks[7]);
					zipsList.Remove(toks[1]);
				}
				
			}

		writeLatLon();
	}


    public static void writeLatLon()
    {

        StreamWriter output = new StreamWriter("LatLon.txt");

        int counter = 0;

        while (counter < latitude.Count())
        {

            output.Write(latitude[counter]);
            output.Write(" ");
            counter++;
            output.Write(latitude[counter]);
            output.Write("\n");
            counter++;

        }

        output.Close();
    } 


    public static void CityStates(){



		  
		StreamWriter output = new StreamWriter("CityStates.txt");
	 	List<String> tempList;
		tempList = citiesList.ConvertAll(d => d.ToUpper());
		citiesList = tempList;

		StreamReader input = new StreamReader("zipcodes.txt");
			
			while (!input.EndOfStream) {
				string line = input.ReadLine();
				string[] toks = line.Split('\t');
				if(citiesList.Contains(toks[3])){
				
					nvc.Add(toks[3], toks[4]);
					
				}
				
			}
	   string[] values = null;


           // need to change this to print keys in VALUES 
           foreach (string key in citiesList) {
		

		List<String> printList = new List<String>();
		
                values = nvc.GetValues(key);

                foreach (string value in values)
                {
                    
		   printList.Add(value);

                } 

		printList.Sort();
		List<String> noDuplicates = printList.Distinct().ToList();
		printList = noDuplicates;


	  

		foreach (string value in printList){
                    
		   output.Write(value);
		   output.Write(" ");

                } // end foreach
 	
		  output.Write("\n");
		

    } 
			
		output.Close();
} 

		
		public static void Main(string[] args){



                populateLists();
		CommonCityNames();
		LatLon();
		CityStates();
		
			
		}



} 





