# -*- coding: utf-8 -*-
# todo
# change ricavi_4_conto_energia
# update spese_5 in funtion of production !!
 

"""
from pathlib import Path
import pandas
from pandas import ExcelFile  
import csv
"""
 
#from xlrd import open_workbook
 
 
# decide: think to the structure... 
 
# source https://it.inflation.eu/tassi-di-inflazione/italia/inflazione-storica/cpi-inflazione-italia.aspx  
INFLATION_RATE_PAST={   2012:  3.04,    
                        2013:  1.22,
                        2014:  0.24,
                        2015:  0.04,
                        2016: -0.09,
                        2017:  1.23,}
 
INFLATION_RATE_FUTURE=  1.1
 
 
class INVESTIMENTO(): 
 
    def __init__(self, inflation_rate, initial_production, first_year,
                 last_year, decrease_rate, used_external_en, perc_autocons,
                 spese_4, incentivo_su_tutta_en_prodotta,
                 incentivo_ssp, eccedenze, incent_5_autocons,
                 incent_5_omnic, incent_5_EU, spese_5):
        self.infl               =   inflation_rate
        self.initial_production =   initial_production
        self.first_year         =   first_year
        self.last_year          =   last_year
        self.decrease_rate      =   decrease_rate
        self.used_external_en   =   used_external_en   
        self.perc_autocons      =   perc_autocons 
        self.spese_4            =   spese_4
        self.incentivo_all_prod =   incentivo_su_tutta_en_prodotta   # =0.236 €/kW·h, \
        self.incentivo_ssp      =   incentivo_ssp                    #  =0.08, change to 0.12 €/kW·h \
        self.eccedenze          =   eccedenze    
        self.incent_5_autocons  =   incent_5_autocons
        self.incent_5_omnic     =   incent_5_omnic
        self.incent_5_EU        =   incent_5_EU
        self.spese_5            =   spese_5
 
    def production_decrease(self, initial_production, first_year, last_year, 
        decrease_rate, accuracy=2, verbose=False ) -> dict:
        """ computed the actual production, create a list with updated values of 
        production, in the consider period (also from future to past)
        """
        production=[initial_production]
        production_dict={first_year:initial_production}
 
        # for i in range(last_year - first_year):
        for i in range(first_year + 1, last_year + 1 , 1 if first_year<last_year else -1):
            if verbose:
                print(i)
            sign_switch = 1 if first_year<last_year else -1    
            decreased_production = round(
                initial_production*(1- (sign_switch)*decrease_rate/100), accuracy )
            production.append( decreased_production )
            production_dict[i] = decreased_production
            initial_production = decreased_production
        if verbose:
            print (production)
            [print("year",k,":", v) for k,v in production_dict.items()]
        return production_dict 
 
    # @staticmethod    
    def each_year_amount_diff(self, verbose=False) -> dict:
        # just the amount difference computed for each of the period
        updated_production=self.production_decrease(self.initial_production, 
            self.first_year, self.last_year, self.decrease_rate, accuracy=2)
        amount_diff_dict={}
 
        for year in range(self.first_year, self.last_year + 1):
            a4= round(self.amount_4_conto_energia(updated_production[year]), 2)
            a5= round(self.amount_5_conto_energia(updated_production[year]), 2)
            if verbose:
                print("a4:", a4, "a5:",a5, "\tdiff:", round(a4-a5,3) )
            amount_diff_dict[year] = ( round(a4-a5,3) )
        if verbose:
            print ( [print("diff value for year", k,":", v, "€/year.") \
                     for k,v in amount_diff_dict.items()] )
 
            """for value in amount_diff_list:
                print ("diff value ", value, " € for year")"""
 
 
        return amount_diff_dict
      
     
    def total_amount_diff_update(self, amount_diff, actual_year,
        number_of_months=None, verbose=False):
         
        tot_p = 0 # total of the past
 
        # finantial ammount update, to move from one year to another
        if verbose:
            print("past years")
        for year in range(self.first_year, actual_year):
            if year == self.first_year:
                partial_year = number_of_months/12
                tot_p=amount_diff[year] if number_of_months==12 else amount_diff[year]*(1-partial_year)
                tot_p = tot_p * ( 1 + INFLATION_RATE_PAST[year]*(1-partial_year)/100)
            else:
                tot_p+= amount_diff[year]
                tot_p = tot_p * \
                    (1 + INFLATION_RATE_PAST[year]/100) 
        print("Past year/s total amount in the past:", tot_p)
 
        print("nowadays year")
        for year in [actual_year]:
            print(year)
            tot_n = amount_diff[year]
            print("Actual year total amount:", tot_n) 
         
        tot_f=0  # total of future
        print("future years")
        for year in range (self.last_year, actual_year, -1):
            print(year)
            if year == self.last_year:
                tot_f= amount_diff[year] if number_of_months==12 else amount_diff[year]*number_of_months/12
                tot_f = tot_f * (1 + \
                 INFLATION_RATE_FUTURE*number_of_months/12/100)
            else:
                tot_f+= amount_diff[year]
                tot_f = tot_f / (1 + INFLATION_RATE_FUTURE/100) 
        print("Past year/s total amount in the past:", tot_f)
 
        return tot_p + tot_n + tot_f    


    def amount_4_conto_energia(self, production, verbose=False):
        """ revenues computation in case of "IV conto energia"
        """
        en_autocons   = round( production * self.perc_autocons) 
        energia_immessa_in_rete =  production - en_autocons
        tot_incentivo_all_prod  =  production * self.incentivo_all_prod
        if en_autocons < self.used_external_en:
            tot_incentivo_ssp   = self.incentivo_ssp * energia_immessa_in_rete
        else:
            tot_incentivo_ssp   = self.incentivo_ssp * energia_immessa_in_rete + \
                self.eccedenze * (en_autocons - self.used_external_en  )
        if verbose:
            print("\nincentivo_ssp: ",self.incentivo_ssp)
            print("incentivo_all_prod: ",self.incentivo_all_prod)
            print("en_autocons   ", en_autocons)  
            print("energia_immessa_in_rete ", energia_immessa_in_rete)
            print("tot_incentivo_all_prod ", tot_incentivo_all_prod) 
            print("tot_incentivo_ssp ", tot_incentivo_ssp)
 
 
        return tot_incentivo_all_prod +  tot_incentivo_ssp - self.spese_4
 
    def amount_5_conto_energia(self, production, verbose=False):
        """ revenues computation in case of "V conto energia"
        """
        en_autocons = round(production*self.perc_autocons,2) 
        energia_immessa_in_rete = round(production - en_autocons, 2)
        tot_incent_autocons = round(en_autocons*self.incent_5_autocons,3)
        tot_incent_omnic = round(self.incent_5_omnic*energia_immessa_in_rete,3)
        tot_incent_EU =  round(production*self.incent_5_EU,2)

        tot_5 = tot_incent_autocons + tot_incent_omnic + tot_incent_EU - self.spese_5
        if verbose:
            print( "production"         , production)
            print( "tot_incent_autocons", tot_incent_autocons)
            print( "tot_incent_omnic"   , tot_incent_omnic)
            print( "tot_incent_EU"      , tot_incent_EU)
            print( "spese"              , spese)
        return tot_5
 
if __name__ == '__main__':
    invest = INVESTIMENTO(inflation_rate=1.1, initial_production=4660,
                             first_year=2012, last_year=2032, decrease_rate=0.55,
                             used_external_en=4050, perc_autocons=0.57,
                             spese_4=45.09, incentivo_su_tutta_en_prodotta=0.236,  # €/kW·h, \
                             incentivo_ssp=0.12,  # change to 0.12 €/kW·h \
                             eccedenze=0.08,
                             incent_5_autocons=0.107,
                             incent_5_omnic=0.189,
                             incent_5_EU=0.02,
                             spese_5=9.82
                          )

    amount_diff=invest.each_year_amount_diff()
    [print(k,v) for k,v in amount_diff.items()]
    tot=invest.total_amount_diff_update(amount_diff, 2018, 8, verbose=True)

    print(tot, "€ in the 20 y.")

    print( "\n\n\tDone!")

