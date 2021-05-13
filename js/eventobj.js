function eventobj(){
    this.events = {}

    this.add_event_listen = function(event, this_argv, mothed){
        if (!this.events[event]){
            this.events[event] = [];
        }
        this.events[event].push({"this_argv":this_argv, "mothed":mothed});
    }

    this.call_event = function(event, argvs){
        if (!this.events[event]){
            return;
        }

        for(var _event of this.events[event]){
            if (!_event["mothed"]){
                continue;
            }
            
            _event["mothed"].apply(_event["this_argv"], argvs);
        }
    }
}
