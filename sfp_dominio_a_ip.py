# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_dominio_a_ip
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      Manuel Jesús Borrero Pedrero
#
# Created:     11/02/2022
# Copyright:   (c) Manuel Jesús Borrero Pedrero
# Licence:     GPL
# -------------------------------------------------------------------------------

import subprocess
from spiderfoot import SpiderFootEvent, SpiderFootPlugin


class sfp_dominio_a_ip(SpiderFootPlugin):

    meta = {
        'name': "Dominio a IP ",
        'summary': "Módulo que dado un dominio devuelve la/las ips de ese dominio con el comando dig",
        'flags': [""],
        'useCases': [""],
        'categories': [""]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    def watchedEvents(self):
        return ["DOMAIN_NAME"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    def producedEvents(self):
        return ["IP_ADDRESS"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:
            
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")
            #Obtenemos con el comando dig la ip
            datos = subprocess.run ('dig +short '+eventData, shell=True, capture_output=True, text=True)
            salida = str(datos.stdout)
            #Guardamos cada ip en ips
            ips=salida.split('\n')
            
            if not ips:
                self.sf.error("Unable to perform <ACTION MODULE> on " + eventData)
                return

        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return

        #Recorremos ips para ir mostrando la/s ips encontradas
        for a in ips:
            evt = SpiderFootEvent(eventName, a, self.__name__, event)
            self.notifyListeners(evt)

# End of sfp_dominio_a_ip class