# -*- coding: utf-8 -*-
"""
:Module: waterapputils_viewer.py

:Author: Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center, http://www.usgs.gov/ 

:Synopsis: Handles views of the data, such as printing and plotting.
"""

__author__   = "Jeremiah Lant, jlant@usgs.gov, U.S. Geological Survey, Kentucky Water Science Center."
__copyright__ = "http://www.usgs.gov/visual-id/credit_usgs.html#copyright"
__license__   = __copyright__
__contact__   = __author__

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from textwrap import wrap

import datetime
import numpy as np
import os
import pdb
        
def print_watertxt_data(watertxt_data):
    """   
    Print information contained in the water data dictionary. 
    
    Parameters
    ----------
    watertxt_data : dictionary 
        A dictionary containing data found in WATER output text file.
    
    Examples
    --------
    >>> import waterapputils_viewer
    >>> import datetime
    >>> import numpy as np
    >>> start_date = datetime.datetime(2014, 04, 01, 0, 0)
    >>> dates = [start_date + datetime.timedelta(i) for i in range(11)]
    >>> discharge_data = np.array([100 + i for i in range(11)])
    >>> subsurfaceflow_data = np.array([i + 2 for i in range(11)])      
    >>> parameters = [{"name": "Discharge (cfs)", "index": 0,
                   ... "data": discharge_data, "mean": np.mean(discharge_data), "max": np.max(discharge_data), 
                   ... "min": np.min(discharge_data)}, 
                      {"name": "Subsurface Flow (mm/day)", "index": 1,
                   ... "data": subsurfaceflow_data, "mean": np.mean(subsurfaceflow_data), "max": np.max(subsurfaceflow_data), 
                   ... "min": np.min(subsurfaceflow_data)}, ]
    >>> data = {user": "jlant", "date_created": "4/9/2014 15:30:00 PM", "stationid": "012345",
            ... "column_names": ["Discharge (cfs)", "Subsurface Flow (mm/day)", "Impervious Flow (mm/day)", "Infiltration Excess (mm/day)", "Initial Abstracted Flow (mm/day)", "Overland Flow (mm/day)", "PET (mm/day)", "AET(mm/day)", "Average Soil Root zone (mm)", "Average Soil Unsaturated Zone (mm)", "Snow Pack (mm)", "Precipitation (mm/day)", "Storage Deficit (mm/day)", "Return Flow (mm/day)"],
            ... "parameters": parameters, "dates": dates}
    >>> waterapputils_viewer.print_info(watertxt_data = data)
    --- DATA FILE INFORMATION ---
    User: jlant
    Date created: 4/9/2014 15:30:00 PM
    StationID: 012345
    Parameters:
      Discharge (cfs)
          mean: 105.0
          max: 100
          min: 110
      Subsurface Flow (mm/day)
          mean: 7.0
          max: 2
          min: 12
    """   
    
    # print relevant information
    print("")
    print("--- DATA FILE INFORMATION ---")
    print("User: {}".format(watertxt_data["user"]))
    print("Date created: {}".format(watertxt_data["date_created"]))
    print("StationID: {}".format(watertxt_data["stationid"]))
    
    print("Parameters:")
    for parameter in watertxt_data["parameters"]:
        print("  {}".format(parameter["name"]))
        print("      mean: {}".format(parameter["mean"]))
        print("      max: {}".format(parameter["max"]))
        print("      min: {}".format(parameter["min"]))
    print("")

def plot_watertxt_data(watertxt_data, is_visible = True, save_path = None):
    """   
    Plot each parameter contained in the nwis data. Save plots to a particular
    path.
    
    Parameters
    ----------
    watertxtdata_data : dictionary 
        A dictionary containing data found in WATER data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    """
    
    for parameter in watertxt_data["parameters"]:
        
        fig = plt.figure(figsize=(12,10))
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.set_title("Parameter: {}\nStationID: {}".format(parameter["name"], watertxt_data["stationid"]))
        ax.set_xlabel("Date")
        ylabel = "\n".join(wrap(parameter["name"], 60))
        ax.set_ylabel(ylabel)
        ax.grid(True)

        if "Discharge" in parameter["name"]:
            color_str = "b"
            
        elif "Subsurface Flow" in parameter["name"]:
            color_str = "g"       
            
        elif "Impervious Flow" in parameter["name"]:
            color_str = "SteelBlue"
            
        elif "Infiltration Excess" in parameter["name"]:
            color_str = "SeaGreen"
            
        elif "Initial Abstracted Flow" in parameter["name"]:
            color_str = "MediumBlue"
                        
        elif "Overland Flow" in parameter["name"]:
            color_str = "RoyalBlue"
                        
        elif "PET" in parameter["name"]:
            color_str = "orange"
                        
        elif "AET" in parameter["name"]:
            color_str = "DarkOrange"
                                    
        elif "Average Soil Root zone" in parameter["name"]:
            color_str = "Gray"
                        
        elif "Average Soil Unsaturated Zone" in parameter["name"]:
            color_str = "DarkGray"
                        
        elif "Snow Pack" in parameter["name"]:
            color_str = "PowderBlue"
            
        elif "Precipitation" in parameter["name"]:
            color_str = "SkyBlue"
            
        elif "Storage Deficit" in parameter["name"]:
            color_str = "k"
                        
        elif "Return Flow" in parameter["name"]:
            color_str = "Aqua"
                        
        else:
            color_str = "k"
                        
        plt.plot(watertxt_data["dates"], parameter["data"], color = color_str, label = ylabel) 
        
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # use a more precise date string for the x axis locations in the
        # toolbar
        ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
     
        # legend; make it transparent    
        handles, labels = ax.get_legend_handles_labels()
        legend = ax.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "mean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter["mean"], parameter["max"], parameter["min"])
        patch_properties = {"boxstyle": "round",
                            "facecolor": "wheat",
                            "alpha": 0.5
                            }
                       
        ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
        
        # save plots
        if save_path:        
            # set the size of the figure to be saved
            curr_fig = plt.gcf()
            curr_fig.set_size_inches(12, 10)
            
            # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
            filename = "-".join([watertxt_data["user"], watertxt_data["stationid"], parameter["name"].split("(")[0]])  + ".png"           
            filepath = os.path.join(save_path, filename)
            plt.savefig(filepath, dpi = 100)                        
          
        # show plots
        if is_visible:
            plt.show()
        else:
            plt.close()

def plot_watertxt_comparison(watertxt_data1, watertxt_data2, is_visible = True, save_path = None):
    """   
    Plot a comparison of two parameters contained in WATER.txt data file. Save 
    plots to a particular path.
    
    Parameters
    ----------
    watertxtdata_data : dictionary 
        A dictionary containing data found in WATER data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s) 
    """
    assert set(watertxt_data1.keys()) == set(watertxt_data2.keys()), "Parameter keys between water datasets do not match"  
    assert set(watertxt_data1["dates"]) == set(watertxt_data2["dates"]), "Dates are not equal"  

    dates = watertxt_data1["dates"]
    for parameter1, parameter2 in zip(watertxt_data1["parameters"], watertxt_data2["parameters"]):    
    
        fig = plt.figure(figsize = (12,10))
        ax1 = fig.add_subplot(211)
        ax1.grid(True)
        ax1.set_title("Parameter: {}\n{} vs {}".format(parameter1["name"], watertxt_data1["stationid"], watertxt_data2["stationid"]))
        ax1.set_xlabel("Date")
        ylabel = "\n".join(wrap(parameter1["name"], 60))
        ax1.set_ylabel(ylabel)
        
        ax1.plot(dates, parameter1["data"], color = "b", label = watertxt_data1["stationid"], linewidth = 2)
        ax1.hold(True)
        ax1.plot(dates, parameter2["data"], color = "r", label = watertxt_data2["stationid"], linewidth = 2, alpha = 0.75)
#        ax1.fill_between(dates, parameter1["data"], parameter2["data"], facecolor = "r", alpha = 0.5)      
        
        # increase y axis to have text and legend show up better
        curr_ylim = ax1.get_ylim()
        ax1.set_ylim((curr_ylim[0], curr_ylim[1] * 1.5))

        # use a more precise date string for the x axis locations in the toolbar
        ax1.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
        
        # legend; make it transparent    
        handles1, labels1 = ax1.get_legend_handles_labels()
        legend1 = ax1.legend(handles1, labels1, fancybox = True)
        legend1.get_frame().set_alpha(0.5)
        legend1.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "mean = %.2f\nmax = %.2f\nmin = %.2f\n---\nmean = %.2f\nmax = %.2f\nmin = %.2f" % (parameter1["mean"], parameter1["max"], parameter1["min"],
                                                                                                  parameter2["mean"], parameter2["max"], parameter2["min"])
        patch_properties = {"boxstyle": "round",
                            "facecolor": "wheat",
                            "alpha": 0.5
                            }
                       
        ax1.text(0.05, 0.95, text, transform = ax1.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
                
        # plot difference = values_b - values_a
        ax2 = fig.add_subplot(212, sharex = ax1)
        ax2.grid(True)
        ax2.set_title("Difference")
        ax2.set_xlabel("Date")
        ax2.set_ylabel(ylabel)
        diff = parameter2["data"] - parameter1["data"]
        ax2.plot(dates, diff, color = "k", linewidth = 2)  
        
        # use a more precise date string for the x axis locations in the toolbar
        ax2.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
        
        # rotate and align the tick labels so they look better; note that ax2 will 
        # have the dates, but ax1 will not. do not need to rotate each individual axis
        # because this method does it
        fig.autofmt_xdate()


        # save plots
        if save_path:        
            # set the size of the figure to be saved
            curr_fig = plt.gcf()
            curr_fig.set_size_inches(12, 10)
            
            # split the parameter name to not include units because some units contain / character which Python interprets as an escape character
            filename = "-".join([watertxt_data1["user"], watertxt_data1["stationid"], " vs ", watertxt_data2["user"], watertxt_data2["stationid"], parameter1["name"].split("(")[0]])  + ".png"           
            filepath = os.path.join(save_path, filename)
            plt.savefig(filepath, dpi = 100)                        
          
        # show plots
        if is_visible:
            plt.show()
        else:
            plt.close()

def print_deltas_data(deltas_data):
    """   
    Print information contained in the delta data dictionary. 
    
    Parameters
    ----------
    watertxt_data : dictionary 
        A dictionary containing data found in WATER output text file.
    """   
   
    print("The following are the parameters and values in the file:")
    
    for key, value in deltas_data.iteritems():
        print("{}: {}".format(key, value))
            
def plot_deltas_data(deltas_data, is_visible = True, save_path = None):
    """   
    Plot each parameter contained in the nwis data. Save plots to a particular
    path.
    
    Parameters
    ----------
    deltasdata_data : dictionary 
        A dictionary containing data found in deltas data file.
    is_visible : bool
        Boolean value to show plots         
    save_path : string 
        String path to save plot(s)
    """

    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Model: " + deltas_data["Model"] + " Scenario: " + deltas_data["Scenario"] + 
                " Target: " + deltas_data["Target"] + " Variable:" + deltas_data["Variable"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Delta Values")
    
    colors_list = ["b", "g", "r", "k", "y", "c", "m", "orange"]
    colors_index = 0
    for tile in deltas_data["Tile"]:        
        tile_index = deltas_data["Tile"].index(tile)
        month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]       
        dates = []        
        data = []
        for month in month_list:
            dates.append(datetime.datetime.strptime(month, "%B"))
            data.append(deltas_data[month][tile_index])
        
        # if the number of tiles exceeds the number of colors in colors list,
        # then randomly pick an rgb color
        if colors_index > len(colors_list) - 1:
            c = np.random.rand(3,)
        else:
            c = colors_list[colors_index]
            
        plt.plot(dates, data, color = c, linestyle = "-", marker = "o", label = tile)
        plt.hold(True)
        
        # rotate and align the tick labels so they look better
        fig.autofmt_xdate()
        
        # set the x axis to display only the month; "%B" => full month name; "%b" => abreviated month name
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%B"))
        
        # legend; make it transparent    
        handles, labels = ax.get_legend_handles_labels()
        legend = ax.legend(handles, labels, fancybox = True)
        legend.get_frame().set_alpha(0.5)
        legend.draggable(state=True)
        
        # show text of mean, max, min values on graph; use matplotlib.patch.Patch properies and bbox
        text = "Model = %s\nScenario = %s\nTarget = %s\nVariable = %s" % (deltas_data["Model"], deltas_data["Scenario"], 
                                                                          deltas_data["Target"], deltas_data["Variable"])
        patch_properties = {"boxstyle": "round",
                            "facecolor": "wheat",
                            "alpha": 0.5
                            }
                       
        ax.text(0.05, 0.95, text, transform = ax.transAxes, fontsize = 14, 
                verticalalignment = "top", horizontalalignment = "left", bbox = patch_properties)
        
        colors_index += 1
        
    # save plots
    if save_path:        
        # set the size of the figure to be saved
        curr_fig = plt.gcf()
        curr_fig.set_size_inches(12, 10)
        filename = deltas_data["Model"] + "_" + deltas_data["Scenario"] + "_" + deltas_data["Target"] + "_" + deltas_data["Variable"]
        plt.savefig(save_path + "/" + filename +".png", dpi = 100)
        
    # show plots
    if is_visible:
        plt.show()
    else:
        plt.close()



def _create_watertxt_test_data(multiplicative_factor = 1, stationid = "012345"):
    """ Create test data for tests """

    dates = [datetime.datetime(2014, 04, 01, 0, 0), datetime.datetime(2014, 04, 02, 0, 0), datetime.datetime(2014, 04, 03, 0, 0)]
    
    discharge_data = np.array([0, 5, 10]) * multiplicative_factor
    subsurface_data = np.array([50, 55, 45]) * multiplicative_factor
    impervious_data = np.array([2, 8, 2]) * multiplicative_factor
    infiltration_data = np.array([0, 1.5, 1.5]) * multiplicative_factor
    initialabstracted_data = np.array([0.1, 0.2, 0.3]) * multiplicative_factor
    overlandflow_data = np.array([3, 9, 3]) * multiplicative_factor
    pet_data = np.array([5, 13, 3]) * multiplicative_factor
    aet_data = np.array([5, 12, 13]) * multiplicative_factor
    avgsoilrootzone_data = np.array([40, 50, 60]) * multiplicative_factor
    avgsoilunsaturatedzone_data = np.array([4, 3, 2]) * multiplicative_factor
    snowpack_data = np.array([150, 125, 25]) * multiplicative_factor
    precipitation_data = np.array([0.5, 0.4, 0.3]) * multiplicative_factor
    storagedeficit_data = np.array([300, 310, 350]) * multiplicative_factor
    returnflow_data = np.array([-5.0, -4.5, -4.0]) * multiplicative_factor
    
    parameters = [{"name": "Discharge (cfs)", "index": 0, "data": discharge_data,
                   "mean": np.mean(discharge_data), "max": np.max(discharge_data), "min": np.min(discharge_data)}, 
                  
                  {"name": "Subsurface Flow (mm/day)", "index": 1, "data": subsurface_data,
                   "mean": np.mean(subsurface_data), "max": np.max(subsurface_data), "min": np.min(subsurface_data)},

                  {"name": "Impervious Flow (mm/day)", "index": 2, "data": impervious_data,
                   "mean": np.mean(impervious_data), "max": np.max(impervious_data), "min": np.min(impervious_data)},

                  {"name": "Infiltration Excess (mm/day)", "index": 3, "data": infiltration_data,
                   "mean": np.mean(infiltration_data), "max": np.max(infiltration_data), "min": np.min(infiltration_data)},

                  {"name": "Initial Abstracted Flow (mm/day)", "index": 4, "data": initialabstracted_data,
                   "mean": np.mean(initialabstracted_data), "max": np.max(initialabstracted_data), "min": np.min(initialabstracted_data)},

                  {"name": "Overland Flow (mm/day)", "index": 5, "data": overlandflow_data,
                   "mean": np.mean(overlandflow_data), "max": np.max(overlandflow_data), "min": np.min(overlandflow_data)},

                  {"name": "PET (mm/day)", "index": 6, "data": pet_data,
                   "mean": np.mean(pet_data), "max": np.max(pet_data), "min": np.min(pet_data)},

                  {"name": "AET (mm/day)", "index": 7, "data": aet_data,
                   "mean": np.mean(aet_data), "max": np.max(aet_data), "min": np.min(aet_data)},

                  {"name": "Average Soil Root zone (mm)", "index": 8, "data": avgsoilrootzone_data,
                   "mean": np.mean(avgsoilrootzone_data), "max": np.max(avgsoilrootzone_data), "min": np.min(avgsoilrootzone_data)},

                  {"name": "Average Soil Unsaturated Zone (mm)", "index": 9, "data": avgsoilunsaturatedzone_data,
                   "mean": np.mean(avgsoilunsaturatedzone_data), "max": np.max(avgsoilunsaturatedzone_data), "min": np.min(avgsoilunsaturatedzone_data)},

                  {"name": "Snow Pack (mm)", "index": 10, "data": snowpack_data,
                   "mean": np.mean(snowpack_data), "max": np.max(snowpack_data), "min": np.min(snowpack_data)},

                  {"name": "Precipitation (mm/day)", "index": 11, "data": precipitation_data,
                   "mean": np.mean(precipitation_data), "max": np.max(precipitation_data), "min": np.min(precipitation_data)},

                  {"name": "Storage Deficit (mm/day)", "index": 12, "data": storagedeficit_data,
                   "mean": np.mean(storagedeficit_data), "max": np.max(storagedeficit_data), "min": np.min(storagedeficit_data)},

                  {"name": "Return Flow (mm/day)", "index": 13, "data": returnflow_data,
                   "mean": np.mean(returnflow_data), "max": np.max(returnflow_data), "min": np.min(returnflow_data)},
    ] 

    data = {"user": "jlant", "date_created": "4/9/2014 15:30:00 PM", "stationid": stationid, 
            "column_names": ["Discharge (cfs)", "Subsurface Flow (mm/day)", "Impervious Flow (mm/day)", "Infiltration Excess (mm/day)", "Initial Abstracted Flow (mm/day)", "Overland Flow (mm/day)", "PET (mm/day)", "AET(mm/day)", "Average Soil Root zone (mm)", "Average Soil Unsaturated Zone (mm)", "Snow Pack (mm)", "Precipitation (mm/day)", "Storage Deficit (mm/day)", "Return Flow (mm/day)"],
            "parameters": parameters, "dates": dates}
    
    return data


def _create_deltas_test_data():
    """ Create a delta data dictionary for tests """

    data = {"Model": "CanESM2", "Scenario": "rcp45", "Target": "2030", "Variable": "PET", "Tile": ["11", "12", "21", "22", "31", "32"],
            "January": [1.3, 1.2, 1.3, 1.4, 1.5, 1.6], "February": [2.7, 2.8, 2.9, 2.3, 2.2, 2.3], "March": [3.3, 3.2, 3.3, 3.4, 3.5, 3.6],
            "April": [4.7, 4.8, 4.9, 4.3, 4.2, 4.3], "May": [5.3, 5.2, 5.3, 5.4, 5.5, 5.6], "June": [6.7, 6.8, 6.9, 6.3, 6.2, 6.3],
            "July": [7.3, 7.2, 7.3, 7.4, 7.5, 7.6], "August": [8.7, 8.8, 8.9, 8.3, 8.2, 8.3], "September": [9.3, 9.2, 9.3, 9.4, 9.5, 9.6],
            "October": [10.7, 10.8, 10.9, 10.3, 10.2, 10.3], "November": [11.3, 11.2, 11.3, 11.4, 11.5, 11.6], "December": [12.7, 12.8, 12.9, 12.3, 12.2, 12.3]           
    }

    return data

    
def test_print_watertxt_data():
    """ Test print output functionality """
    
    print("---Testing print_watertxt_data ---")
    
    data = _create_watertxt_test_data()
    print_watertxt_data(watertxt_data = data)
    
    print("")

def test_plot_watertxt_data():
    """ Test plot_watertxt_data functionality """
    
    print("--- Testing plot_watertxt_data ---")    
    
    data = _create_watertxt_test_data()
    plot_watertxt_data(watertxt_data = data, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")

def test_plot_watertxt_comprison():
    """ Test plot_watertxt_comprison functionality """
    
    print("--- Testing plot_watertxt_comprison ---")    
    
    data1 = _create_watertxt_test_data()
    data2 = _create_watertxt_test_data(multiplicative_factor = 2, stationid = "00000")
    plot_watertxt_comparison(watertxt_data1 = data1, watertxt_data2 = data2, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")


def test_print_deltas_data():
    """ Test print output functionality """
    
    print("---Testing print_deltas_data ---")
    
    data = _create_deltas_test_data()
    print_deltas_data(deltas_data = data)
    
    print("")
    
def test_plot_deltas_data():
    """ Test plot_deltas_data functionality """
    
    print("--- Testing plot_deltas_data ---")    
    
    data = _create_deltas_test_data()
    plot_deltas_data(deltas_data = data, is_visible = True, save_path = None)
    
    print("Plotting completed")
    print("")
    
def main():
    """ Test functionality of waterapputils_viewer """

    print("")
    print("RUNNING TESTS ...")
    print("")
    
#    test_print_watertxt_data()
#    
#    test_plot_watertxt_data()
    
#    test_plot_watertxt_comprison()    

    test_plot_deltas_data()
    
    test_print_deltas_data()

if __name__ == "__main__":
    main() 