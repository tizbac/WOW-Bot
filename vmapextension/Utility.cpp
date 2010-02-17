#include <iostream>
#include <string>
#include <map>
#include <stdlib.h>
#include <vector>
#include <stdarg.h>
#include <execinfo.h>
#include <errno.h>
#include <signal.h>
#include <sys/time.h>

#include "Utility.h"
using namespace std;
extern bool deb;
std::string strfmt(std::string fmt,...)
{
  char msgF[4096];
  va_list args;
  va_start(args,fmt);
  vsnprintf(msgF,4096,fmt.c_str(),args);
  return std::string(msgF);
}
void printstacktrace()
{
  void *array[100];
  size_t size;
  size = backtrace(array, 100);
  char ** bt = backtrace_symbols(array, size);
  for ( int i = 0; i < size;i++)
  {
    debug("Debug StackTrace: %s",bt[i]);
  }
}
void printlastcall()
{
  void *array[100];
  size_t size;
  size = backtrace(array, 100);
  char ** bt = backtrace_symbols(array, size);
  debug("Debug StackTrace: %s",bt[0]);

  
}
double getcurrenttime()
{
  struct timeval t;
  gettimeofday(&t,NULL);
  double ti = 0.0;
  ti = t.tv_sec;
  ti += t.tv_usec/1000000.0;
  return ti;
}
void error(std::string msg,...)
{
  char msgF[4096];
  va_list args;
  va_start(args,msg);
  vsnprintf(msgF,4096,msg.c_str(),args);
  cout << "\033[21;31m[ERROR ]\033[0m " << msgF << endl;
}
void debug(std::string msg,...)
{
  if ( deb)
  {
    char msgF[4096];
    va_list args;
    va_start(args,msg);
    vsnprintf(msgF,4096,msg.c_str(),args);
    cout << "\033[21;34m[DEBUG ]\033[0m " << msgF << endl;
  }
}
void info(std::string msg,...)
{
  char msgF[4096];
  va_list args;
  va_start(args,msg);
  vsnprintf(msgF,4096,msg.c_str(),args);
  cout << "\033[21;35m[ INFO ]\033[0m " << msgF << endl;
}
void notice(std::string msg,...)
{
  char msgF[4096];
  va_list args;
  va_start(args,msg);
  vsnprintf(msgF,4096,msg.c_str(),args);
  cout << "\033[21;36m[NOTICE]\033[0m " << msgF << endl;
}
void good(std::string msg,...)
{
  char msgF[4096];
  va_list args;
  va_start(args,msg);
  vsnprintf(msgF,4096,msg.c_str(),args);
  cout << "\033[21;32m[ GOOD ]\033[0m " << msgF << endl;
}
void bad(std::string msg,...)
{
  char msgF[4096];
  va_list args;
  va_start(args,msg);
  vsnprintf(msgF,4096,msg.c_str(),args);
  cout << "\033[21;33m[  BAD ]\033[0m " << msgF << endl;
}
char * signalname(int s)
{
  std::string sn;
  char snc[1024];
  switch(s)
  {
    case SIGABRT:
      sn = "Abort";
      break;
    case SIGSEGV:
      sn = "Segmentation Fault";
      break;
    case SIGHUP:
      sn = "Hangup";
      break;
    case SIGINT:
      sn = "Keyboard Interrupt";
      break;
    case SIGTERM:
      sn = "Terminated";
      break;
    case SIGILL:
      sn = "Illegal Instruction";
      break;
    case SIGFPE:
      sn = "Floating point exception";
      break;
    /*case SIGEMT:
      sn = "Emulate instruction violated";
      break;*/
    case SIGBUS:
      sn = "Bus error";
      break;
    case SIGSYS:
      sn = "Bad argument to system call";
      break;
    case SIGQUIT:
      sn = "Quit";
      break;
    case SIGSTKFLT:
      sn = "Stack Fault";
      break;
    case SIGPWR:
      sn = "Power failure";
      break;
    default:
      sn = "Unknown Signal";
      break;
  }
  snprintf(snc,1024,"%s",sn.c_str());
  return (snc);
}
char * geterror()
{
  debug("GetError()");
  std::string err;
  char erro[1024];
  switch (errno)
  {
    case 0:
      err = "No error";
      break;
    case E2BIG:
      err = "Argument list too long.";
      break;
  //  case EACCESS:
  //    err = "Permission denied";
      //break;
    case EADDRINUSE:
      err = "Address already in use";
      break;
    case EADDRNOTAVAIL:
      err = "Address not available";
      break;
    case EAFNOSUPPORT:
      err = "Address family not supported";
      break;
    case EAGAIN:
      err = "Resource temporarily unavaible";
      break;
    case EALREADY:
      err = "Connection already in progress";
      break;
    case EBADF:
      err = "Bad file descriptor";
      break;
    case EBADMSG:
      err = "Bad Message";
      break;
    case EBUSY:
      err = "Device or resource busy";
      break;
    case ECANCELED:
      err = "Operation canceled";
      break;
    case ECHILD:
      err = "No child processes";
      break;
    case ECONNABORTED:
      err = "Connection aborted";
      break;
    case ECONNREFUSED:
      err = "Connection refused";
      break;
    case ECONNRESET:
      err = "Connection reset by peer";
      break;
    case EDEADLK:
      err = "Resource deadlock would occour";
      break;
   // case EDESTADDREQ:
   //   err = "Destination address required";
      break;
    case EDOM:
      err = "Mathematics argument out of domain of function";
      break;
    case EDQUOT:
      err = "Reserved";
      break;
    case EEXIST:
      err = "File exists";
      break;
    case EFAULT:
      err = "Bad address";
      break;
    case EFBIG:
      err = "File too large";
      break;
    case EHOSTUNREACH:
      err = "Host is unreachable";
      break;
    case EIDRM:
      err = "Identifier removed";
      break;
    case EILSEQ:
      err = "Illegal byte sequence";
      break;
    case EINPROGRESS:
      err = "Operation in progress";
      break;
    case EINTR:
      err = "Interrupted function";
      break;
    case EINVAL:
      err = "Invalid argument";
      break;
    case EIO:
      err = "I/O Error";
      break;
    case EISCONN:
      err = "Socket is connected";
      break;
    case EISDIR:
      err = "Is a directory";
      break;
    case ELOOP:
      err = "Too many levels of symbolic links";
      break;
    case EMFILE:
      err = "Too many open files";
      break;
    case EMLINK:
      err = "Too many links";
      break;
    case EMSGSIZE:
      err = "Message too large";
      break;
    case EMULTIHOP:
      err = "Reserved";
      break;
    case ENAMETOOLONG:
      err = "Filename too long";
      break;
    case ENETDOWN:
      err = "Network is down";
      break;
    case ENETRESET:
      err = "Connection aborted by network";
      break;
    case ENETUNREACH:
      err = "Network unreachable";
      break;
    case ENFILE:
      err = "Too many open files in system";
      break;
    case ENOBUFS:
      err = "No buffer space avaible";
      break;
    case ENODATA:
      err = "No data on stream";
      break;
    case ENODEV:
      err = "No such device";
      break;
    case ENOENT:
      err = "No such file or directory";
      break;
    case ENOEXEC:
      err = "Executable file format error";
      break;
    case ENOLCK:
      err = "No locks avaible";
      break;
    case ENOLINK:
      err = "Reserved";
      break;
    case ENOMEM:
      err = "Not enough space";
      break;
    case ENOMSG:
      err = "No message";
      break;
    case ENOPROTOOPT:
      err = "Protocol not avaible";
      break;
    case ENOSPC:
      err = "No space left on device";
      break;
    case ENOSR:
      err = "No stream resources";
      break;
    case ENOSTR:
      err = "Not a stream";
      break;
    case ENOSYS:
      err = "Functon not supported";
      break;
    case ENOTCONN:
      err = "The socket is not connected";
      break;
    case ENOTDIR:
      err = "Not a directory";
      break;
    case ENOTEMPTY:
      err = "Directory not empty";
      break;
    case ENOTSOCK:
      err = "Not a socket";
      break;
    case ENOTSUP:
      err = "Not supported";
      break;
    case ENOTTY:
      err = "Inappropriate I/O control operation";
      break;
    case ENXIO:
      err = "No such device or address";
      break;
   // case EOPNOTSUPP:
   //   err = "Operation not supported on socket";
      break;
    case EOVERFLOW:
      err = "Value too large to be stored in data type";
      break;
    case EPERM:
      err = "Operation not permitted";
      break;
    case EPIPE:
      err = "Broken pipe";
      break;
    case EPROTO:
      err = "Protocol error";
      break;
    case EPROTONOSUPPORT:
      err = "Protocol not supported";
      break;
    case EPROTOTYPE:
      err = "Protocol wrong type for socket";
      break;
    case ERANGE:
      err = "Result too large";
      break;
    case EROFS:
      err = "Read-only file system";
      break;
    case ESPIPE:
      err = "Invalid seek";
      break;
    case ESRCH:
      err = "No such process";
      break;
    case ESTALE:
      err = "Reserved";
      break;
    case ETIME:
      err = "Operation timed out";
      break;
    case ETXTBSY:
      err = "Text file busy";
      break;
   // case EWOULDBLOCK:
    //  err = "Operation would block";
      break;
    case EXDEV:
      err = "Cross-device link.";
      break;
    
    default:
      err = "Unknown error code";
  }
  snprintf(erro,1024,"%s",err.c_str());  
    
  return (erro);  
  }
void printvectorS(std::vector<std::string> vec)
{
  std::vector<std::string>::iterator it;
  cout << "Vector: [";
  for ( it = vec.begin();it < vec.end();it++)
    cout << *it << "(" << (*it).length() << ")" << ",";
  cout << "]" << endl;
  
}
std::vector<std::string> split(std::string s,std::string d)
{
  std::string s2(s);
  std::vector<std::string> v;
  while ( s2.find(d) != string::npos)
  {
    
    v.push_back(s2.substr(0,s2.find(d)));
    s2 = s2.substr(s2.find(d)+1,-1);
  }
  if ( s2.length() > 0 )
  {
    v.push_back(s2);
  }
 // printvectorS(v);
  return v;
  
}
string join(vector<string> ar,int start)
{
  vector<string>::iterator it;
  string str;
  for ( it=ar.begin()+start; it < ar.end(); it++)
  {
   str.append(*it+" ");
  }
  str.erase(str.length()-1,1);
  return str;
}
void delchr(char c, string &s){
std::string::size_type k = 0;
while((k=s.find(c,k))!=s.npos) {
s.erase(k, 1);
}
}
std::string getfiledata(char * filename)
{
  FILE * f;
  f = fopen(filename,"r");
  if (not f)
  {
    error("Cannot load file "+string(filename));
    return std::string("FAIL");
  }
  int s = 0;
  char * data;
  fseek(f,0,SEEK_END);
  s = ftell(f);
  fseek(f,0,SEEK_SET);
  data = (char*)malloc(s+1);
  fread(data,s,1,f);
  fclose(f);
  data[s] = 0;
  return std::string(data);
}
