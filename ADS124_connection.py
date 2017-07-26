from abc import ABCMeta, abstractmethod

class ADS124_connection:
   """
   Abstract base class for ADS124 connections.

   Must be re-implemented with the given methods to fit the desired connection type.
   """
   __metaclass__ = ABCMeta

   @abstractmethod
   def ADS124_transfer(self,list):
      pass
   def ADS124_connect(self):
      pass
   def ADS124_close(self):
      pass
