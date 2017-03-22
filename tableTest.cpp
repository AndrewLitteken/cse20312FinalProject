/*
	tableTest.cpp
	Proof of concept of using a table to select items to be used later
	Author: Andrew Litteken
	Data: 2017-03-22
*/

#include <iostream>
#include <vector>
using namespace std;

int useTable(vector<int> weights, vector<int> scores){
	int finalScore = 0; // intitalize score
	for (int i=0;i<scores.size();i++){ // cycle through the scores and weights
		finalScore = finalScore+weights[i]*scores[i]; // for each score and weight, multiply items and add to final score
	}
	return finalScore; // return the final score
}

int main(){
	int option;
	int threshold=105; // threshold score to be included
	cout<<"Pick an option (1-3) to organize items: "; // have the user pick a set of weightings
	cin >> option;
	vector<int> weights;
	switch (option) { // Set the weightings to one of the following options
		case 1:
			weights.push_back(8);
			weights.push_back(6);
			weights.push_back(4);
			break;
		case 2:
			weights.push_back(6);
			weights.push_back(8);
			weights.push_back(4);
			break;
		case 3:
			weights.push_back(4);
			weights.push_back(6);
			weights.push_back(8);
			break;
		default:
			weights.push_back(5);
			weights.push_back(5);
			weights.push_back(5);
			break;
	}
	vector< vector<int> > scores;
	vector<int> scoreSet1 = {5, 6, 7};  // Load the different vectors of scores
	vector<int> scoreSet2 = {6, 5, 7}; 
	vector<int> scoreSet3 = {7, 5, 6};
	scores.push_back(scoreSet1); // Add scores set to the overall scores vector
	scores.push_back(scoreSet2);
	scores.push_back(scoreSet3);
	int length = scores.size();
	int totalScores[length];
	for(int i=0;i<length;i++){ // cycle through the score sets
		totalScores[i]=useTable(weights, scores[i]); // Calculate overall score for each object being analyzed
		if (totalScores[i]>=threshold) cout<<"Item "<<i+1<<" with score "<<totalScores[i]<<" is included"<<endl;
		else cout<<"Item "<<i+1<<" with score "<<totalScores[i]<<" is not included"<<endl; // display resutls
	}
	// Some sorting/Decision making happens here to say what is included and what is not
	// In the real project, if nothing is found, maybe supplement with other stuff outside of the user's library
}
