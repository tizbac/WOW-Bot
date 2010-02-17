#ifndef THREAD_H
#define THREAD_H
#include <pthread.h>
#include <iostream>
#include <map>
#include "Utility.h"
#include <stdlib.h>
#include <signal.h>
using namespace std;
namespace Threading {
class Thread{
  public:
  pthread_t tid;
  
  Thread(void *(*f)(void *),void * arg);
  void Kill();
  void Join();
};
class Mutex{
  public:
  pthread_mutex_t mid;
  Mutex();
  void Lock();
  void UnLock();
  void TryLock();
  
};}
#endif