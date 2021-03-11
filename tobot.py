import os
from pydbus import SystemBus
from gi.repository import GLib
import functools

bus = SystemBus()
loop = GLib.MainLoop()

send_str = "~/.signal-cli/signal-cli-0.8.1/bin/signal-cli send -m {message} {recipient}"

signal = bus.get('org.asamk.Signal')

items = []

def add_item(args):
    if len(args) == 0:
        return "Kein TOP angegeben: /addTOP <TOP>"
    elif len(args) == 1:
        items.append(args[0])
        return "TOP {item} hinzugefügt!".format(item = args[0])
    else:
        items.extend(args)
        return "TOPS {args} hinzugefügt!".format(args = functools.reduce(lambda x, y: x + ", " + y, args))

def delete_item(args):
    if len(args) == 0:
        return "Kein TOP angegeben: /delTOP <TOP>"
    elif len(args) == 1:
        item = args[0]
        ret_str = "TOP {item} enfernt".format(item = item)
        if item not in items:
            ret_str = "TOP {item} befindet sich garnicht auf der TO".format(item=item)
        items.remove(item)
        return ret_str
    else:
        #TODO besser machen
        return "Bitte immer nur ein TOP gleichzeitig löschen"


def clear_list(args):
    items.clear()
    return "TO zurückgesetzt"

def list_to_str(args):
    if len(items) == 0:
        return "Leer"
    return functools.reduce(lambda x,y: x + "\n" + y, items, "TO:")


def help(args):
    help_str = """Übersicht der Befehle an den TOBot. Diese können einfach als Signal-Nachricht in die Gruppe geschrieben werden.
TO anzeigen:        /TO
TOP hinzufügen:     /addTOP <TOP>
TOP löschen:        /delTOP <TOP>
TO zurücksetzen:    /newTO 
Hilfetext anzeigen: /help"""
    return help_str

def msgRcv(timestamp, source, groupID, message, attachments):
    args = message.split(" ")

    switcher = {
        "/addTOP"   : add_item,
        "/delTOP"   : delete_item,
        "/TO"       : list_to_str,
        "/newTO"    : clear_list,
        "/help"     : help
    }
    func = switcher.get(args[0])

    # Kein Befehl an Bot, dieser darf aus maximal zwei wörtern bestehen
    if func is None or len(args) > 2:
        print("Kein Befehl")
        return

    ret_str = func(args[1:])

    signal.sendMessage(ret_str, [], [source])
    return


signal.onMessageReceived = msgRcv

loop.run()



#os.system(send_str.format(message = "huhu", recipient = "+4915120642966"))


