
#include "Thread.h"
namespace Threading{
Thread::Thread(void *(*f)(void *),void * arg)
{
  debug("Spawning new thread");
  int err = pthread_create(&tid,NULL,f,arg);
  if ( err != 0)
  {
    error("FATAL: Thread failed to spawn");
    abort();
  }
  
}
void Thread::Join()
{
  pthread_join(tid,NULL);
}
void Thread::Kill()
{
 // pthread_kill(tid,SIGHUP); Epic fail
}

Mutex::Mutex()
{
  if (pthread_mutex_init(&mid,NULL) != 0)
  {
    error("Cannot create mutex");
  }
}
void Mutex::Lock()
{
  pthread_mutex_lock(&mid);
}
void Mutex::UnLock()
{
  pthread_mutex_unlock(&mid);
}
void Mutex::TryLock()
{
   pthread_mutex_trylock(&mid);
}}
  
