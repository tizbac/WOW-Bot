#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <stdio.h>
void printlastcall();
void printstacktrace();
using namespace std;
void error(std::string msg,...);
void debug(std::string msg,...);
void info(std::string msg,...);
void notice(std::string msg,...);
void good(std::string msg,...);
void bad(std::string msg,...);
std::string strfmt(std::string fmt,...);
char * geterror();
string join(vector<string> ar,int start);
void delchr(char c, string &s);
std::vector<std::string> split(std::string s,std::string d);
std::string getfiledata(char * filename);
char * signalname(int s);
double getcurrenttime();
