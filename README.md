Calvin Tang ct541
Christina Yang csy28

0. Please write down the full names and netids of all your team members.
1. Briefly discuss how you implemented your recursive root and TLD server
   functionality.
2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.
3. What problems did you face developing code for this project?
4. What did you learn by working on this project?

--------------------------------------------------------------------------------------------------------------------------------

1.We implemented the root server by setting up a socket that would accept a connection from the client program and sockets that would initiate connections with the TLD servers, whose addresses were found by parsing the input file given to the root server. The client would send queries to the root server, where the root server would first check if the query was in its DNS table. If the query was present, then it would return a string to the client containing its version of the queried hostname. If the query was not present, then it would parse the query and see if the query ended in .com or .edu. If it did, then it would just forward the query to the corresponding TLD server to deal with, and once it got a response, forward the response back to the client. If the query was not in the root server DNS table or had a .com or .edu ending, then the root server would send an error message back to the client. In regards to the TLD servers, they would accept a connection from the root server, perform lookups on the queried hostnames and send error messages if unsuccessful or its version of the queried hostname back to root server otherwise. 
2.To the best of our knowledge, there are no known issues or problems with our code
3.The project was very similar to the previous project so there were no problems. 
4.We expanded upon our knowledge of how root servers and top level domain servers worked. We learned how to work with a root server that accepted client connections and initiated client connections with the TLD servers. Additionally, we learned that by parsing the query can make the whole lookup process more efficient in that we now send strings with specific suffixes to the corresponding TLD server. 
