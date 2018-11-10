# -*- coding: utf-8 -*-
import unittest
import FV as FV
 
INFLATION_RATE_PAST={   2012:  3.04,
                        2013:  1.22,
                        2014:  0.24,
                        2015:  0.04,
                        2016: -0.09,
                        2017:  1.23,}
INFLATION_RATE_FUTURE=  1.1
 
invest=FV.INVESTIMENTO(inflation_rate=1.1, initial_production=4660,
            first_year=2012, last_year=2032, decrease_rate=0.55,
            used_external_en=4050, perc_autocons=0.57, 
            spese_4=45.09, incentivo_su_tutta_en_prodotta=0.236,  # €/kW·h, \
                               incentivo_ssp=0.12,   # change to 0.12 €/kW·h \
                               eccedenze=0.08, 
            incent_5_autocons=0.107, 
            incent_5_omnic=0.189,
            incent_5_EU=0.02,
            spese_5=9.82
                       )
 
class TestStringMethods(unittest.TestCase):
    def setUp(self):
        pass
 
 
    def test_each_year_amount_diff(self, verbose=False):
        # just the ammount difference computed for each of the period 
         
        # first year test
        self.assertAlmostEqual(  548.81, 
        invest.each_year_amount_diff(verbose)[2012],1)   #  548,81 €/anno
        # last year difference   based on 4177.09 kW·h/y, expected  478,63  €/anno
        self.assertAlmostEqual(  478.053, 
        invest.each_year_amount_diff(
                               #verbose=True
                               )[2032],1)   #   478,63  €/anno 
 
 
 
    def test_production_decrease(self):
        self.assertAlmostEqual(invest.production_decrease(4660,
                               2012, 2032, 0.545511509695109, 
                               accuracy=3, 
                               #verbose=True
                               )[2032], 4177.088)   # 1214.97
        #test just one year interval
        self.assertAlmostEqual(invest.production_decrease(4660, 
                               2018, 2018, 0.55, 
                               # verbose=True
                               )[2018], 4660)   # 1214.97
        # todo case from future to past
        """
        self.assertAlmostEqual(invest.production_decrease(4177.088, 
                               2032, 2012, 0.55, accuracy=3,
                               verbose=True
                               )[2031], 4661.387)   # 1214.97  -1
        """
 
    def test_total_amount_diff_update(self, verbose=False):

        invest.each_year_amount_diff(verbose=True)

        self.assertAlmostEqual(8086.59,
            invest.total_amount_diff_update(
                    invest.each_year_amount_diff(
                        verbose=True
                                                 ),
                    2018, 8,
                               # verbose=True
                               ), 1)    # 11595.06 
 
        # finantial ammount update, to move from one year to another
        static=440
        amount_diff_dict={}
        for i in range(2012,2033):
            amount_diff_dict[i]=static     
        if verbose: 
            print(amount_diff_dict)
            print (len(amount_diff_dict ) )
 
        self.assertAlmostEqual(8086.59, 
            invest.total_amount_diff_update(amount_diff_dict, 2018, 8,
                               # verbose=True
                               )[-1], 1)   # 1214.97
 
    """    
    def test_value_update(self):
        # 2031  440  730,14  722,20 1,1      730,14  722,20
        self.assertEqual(invest.value_update(440, 2018, 2018), 440)   # 1214.97
 
        self.assertAlmostEqual(invest.value_update(440, 2032, 2031, 8),  290.14, 2)   #  290,14 
 
        self.assertEqual(invest.value_update(440, 2031,2018), 722.2)   # 1214.97
        # or years, number_of_months=None):
    """
 
    def test_ricavi_4_conto_energia(self):
        self.assertAlmostEqual(1295.13,
             invest.amount_4_conto_energia(4660),1)   # 1214.97
        self.assertAlmostEqual( 386.31,
             invest.amount_4_conto_energia(1500,verbose=False),1)   # 1214.97
 
 
        invest.incentivo_ssp=0.08    # old value
        self.assertAlmostEqual(1214.99,
             invest.amount_4_conto_energia(4660, verbose=False),1)   # 1214.97
 
        invest.incentivo_all_prod=.277
        self.assertAlmostEqual(1406.03,
             invest.amount_4_conto_energia(4660, verbose=False),1)   # 1214.97
 
 
    def test_ricavi_5_conto_energia(self, verbose=False):

        invest.perc_autocons = .57
        invest.incentivo_ssp = 0.12
        self.assertAlmostEqual(746.38,
                               invest.amount_5_conto_energia(4660), 0)  # from data_sheet  746,3116  €/anno

        invest.perc_autocons=.57
        invest.incentivo_ssp=0.08
        self.assertAlmostEqual(746.38, 
             invest.amount_5_conto_energia(4660), 0)   # from data_sheet  746,3116  €/anno 
        self.assertAlmostEqual(510.2, 
             invest.amount_5_conto_energia(3000, verbose=False ), 1)   # from data_sheet  510,16  €/anno
 
        invest.perc_autocons=.70
        self.assertAlmostEqual(696.38, 
            invest.amount_5_conto_energia(4660), 0)   # 696,636  €/anno
 
 
if __name__ == '__main__':
    # unittest.main()
    unittest.main(exit=False)  # https://stackoverflow.com/questions/9202772/tests-succeed-still-get-traceback

