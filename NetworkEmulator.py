#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 13:49:58 2020

@author: mep53
"""
import docker
import time
from Logger import Logger
import hiyapyco

class NetworkEmulator(object):    
    def __init__(self,client,client_low,ntw,config):
        self.ntw =ntw
        self.run_base_label = config['run']['run_base_label']
        self.client = client
        self.client_low = client_low
        self.mnscripts_vol = "/home/mep53/workspace/scala/ngcdi/mperhez/ryu-sdn-mininet/mnscripts"
                ########SDNC Parameters ########
        self.sdnc_img = "mperhez/ryu-sdn-controller:latest"
        self.sdnc_label = "ryu-sdn"
        self.sdnc_command = ""
        self.sdnc_mem_limit = "500m" 
        self.sdnc_mem_res = "450m"
            #ifxdb_mem_limit = "1g" 
            #ifxdb_mem_res = "900m"
        self.sdnc_env = {}
        sdnc_port = "8080"
        self.sdnc_ports = {sdnc_port: sdnc_port}
            
            ########Mininet Parameters ########
        self.mnet_img = "mperhez/mininet:latest"
        self.mnet_label = "mnet"
        self.mnet_command = ""
        self.mnet_mem_limit = "500m" 
        self.mnet_mem_res = "450m"
            #ifxdb_mem_limit = "1g" 
            #ifxdb_mem_res = "900m"
        self.mnet_env = {}
        mnet_port = "9081"
        self.mnet_ports = {mnet_port:mnet_port}
        self.mnet_script = "py-mininet.py"
        
        ########Test Controller Server Parameters ########
        self.tcs_img = "mperhez/flask_tcs:latest"
        self.tcs_label = "tcs"
        self.tcs_script = "/reroute/MyTestServer.py"
        self.tcs_command = ""#"python3 "+tcs_script
        self.tcs_mem_limit = "500m" 
        self.tcs_mem_res = "450m"
        self.tcs_env = {}
        tcs_port = "5000"
        self.tcs_ports = {tcs_port:tcs_port}
        self.tcs_vol = "/home/mep53/workspace/scala/ngcdi/mperhez/test-api-server/onos-reroute-api/testClient"
        
    def emu_network_inf(self,ntw,run_label,mnet_n,sdnc_n):
        ninf_ids = []
        
        for i in range(1,sdnc_n+1):
            sdnc_vols = {
                    self.mnscripts_vol: {"bind": "/mnscripts", 'mode': "rw"}
                    }
            
            lmsg = run_label + ":" + "vol sdn_ntw: " + str(sdnc_vols)
            
            Logger.get_logger(self.run_base_label).info(lmsg)
            lmsg = run_label + ":" + "vars sdn_ntw: " + str(self.sdnc_env)
            Logger.get_logger(self.run_base_label).info(lmsg)
            
            sdnc = self.client.containers.run(self.sdnc_img,
                              self.sdnc_command, 
                              name = self.sdnc_label+"-"+str(i),
                              auto_remove = False,
                              detach = True,
                              mem_limit = self.sdnc_mem_limit,
                              mem_reservation = self.sdnc_mem_res,
                              network = ntw.name,
                              volumes = sdnc_vols,
                              ports = self.sdnc_ports,
                              environment = self.sdnc_env
                              )
            
            
            # Obtain Controller IP to pass to mnet, could not do it with docker high_level api
            sdn_details = self.client_low.inspect_container(sdnc.id)
            self.sdnc_ip = sdn_details.get("NetworkSettings").get("Networks").get(ntw.name).get("IPAddress")
            
            ninf_ids.append(sdnc.id) 
        
        lmsg = run_label + ":" + "sdnc created..." + str(ninf_ids)
        Logger.get_logger(self.run_base_label).info(lmsg)
        
        if(sdnc_n > 0):time.sleep(5)
        
        mnet_env = {
                    "MN_SCRIPT": self.mnet_script,
                    "SDN_C1": self.sdnc_ip
                }
        for i in range(1,mnet_n+1):
            mnet_vols = {
                   self.mnscripts_vol: {"bind": "/mnscripts", 'mode': "rw"}
                    }
            
            lmsg = run_label + ":" + "vol mnet_ntw: " + str(mnet_vols)
            Logger.get_logger(self.run_base_label).info(lmsg)
            lmsg = run_label + ":" + "vars mnet_ntw: " + str(mnet_env)
            Logger.get_logger(self.run_base_label).info(lmsg)
            
            mnet = self.client.containers.run(self.mnet_img,
                              self.mnet_command, 
                              name = self.mnet_label+str(i),
                              auto_remove = False,
                              detach = True,
                              privileged = True,
                              mem_limit = self.mnet_mem_limit,
                              mem_reservation = self.mnet_mem_res,
                              network = ntw.name,
                              volumes = mnet_vols,
                              ports = self.mnet_ports,
                              environment = mnet_env
                              )
            ninf_ids.append(mnet.id) #ifxdb is the head
              
        lmsg = run_label + ":" + " mnet created..." + str(ninf_ids)
        Logger.get_logger(self.run_base_label).info(lmsg)
        
        return ninf_ids

    def test_controller_server(self,run_label):
        ninf_ids = []
        tcs_vols = {
                    self.tcs_vol: {"bind": "/reroute", 'mode': "rw"}
                    }
        tcs_env = {
                        "TCS_SCRIPT": self.tcs_script,
                        "FLASK_APP": self.tcs_script,
                        "FLASK_ENV":"development",
                        "FLASK_DEBUG":"1"
                    }
        
        lmsg = run_label + ":" + "vol tcs_ntw: " + str(tcs_vols)
        Logger.get_logger(self.run_base_label).info(lmsg)
        lmsg = run_label + ":" + "vars tcs_ntw: " + str(tcs_env)
                
                
        tcs = self.client.containers.run(self.tcs_img,
                                  self.tcs_command, 
                                  name = self.tcs_label,
                                  auto_remove = False,
                                  detach = True,
                                  privileged = True,
                                  mem_limit = self.tcs_mem_limit,
                                  mem_reservation = self.tcs_mem_res,
                                  network = self.ntw.name,
                                  volumes = tcs_vols,
                                  ports = self.tcs_ports,
                                  environment = tcs_env
                                  )
        ninf_ids.append(tcs.id) 
                  
        lmsg = run_label + ":" + " test server created..." + str(ninf_ids)
        Logger.get_logger(self.run_base_label).info(lmsg)
            
        return ninf_ids

def main():
    client = docker.from_env() #Needs to be here because of threading, TODO: check later 
    client_low = docker.APIClient(base_url='unix://var/run/docker.sock') # low level api
    ntw_name = "mininet_default"
    ntw = client.networks.get(ntw_name)
    print(ntw.name)
    
    base_dir = '/home/mep53/workspace/scala/ngcdi/mperhez/ryu-sdn-mininet/'
    
    config = hiyapyco.load( # Order is important the latest files override the first ones
                 base_dir+'resources/base_config.yaml',
                 base_dir+'resources/net_emu_config.yaml'
             )
    
    ne = NetworkEmulator(client,client_low,ntw,config)
    mnet_n = 1
    sdnc_n = 1
    run_base_label = "datest1"
    run_label = "1"

    ne.emu_network_inf(ntw, run_label, mnet_n, sdnc_n)

if __name__ == '__main__':
    main() 