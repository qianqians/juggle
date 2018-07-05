function juggle_process(){
    this.module_set = {};

    this.event_set = [];
    this.add_event = [];
    this.remove_event = [];

    this.reg_channel = function(ch){
        this.add_event.push(ch);
    }

    this.unreg_channel = function(ch){
        this.remove_event.push(ch);
    }

    this.reg_module = function(_module){
		this.module_set[_module.module_name] = _module;
    }

    this.poll = function(){
        for(ch in this.add_event)
        {
            this.event_set.push(this.add_event[ch]);
        }
        this.add_event = [];

        var _new_event_set = new [];
        for(_ch in this.event_set)
        {
            var in_remove_event = false;
            for(ch in this.remove_event)
            {
                if (this.event_set[_ch] === this.remove_event[ch])
                {
                    in_remove_event = true;
                    break;
                }
            }
            if (!in_remove_event)
            {
                _new_event_set.push(this.event_set[_ch]);
            }
        }
        this.event_set = _new_event_set;
        this.remove_event = [];

        _new_event_set = new [];
        while(this.event_set.length > 0)
        {
            var ch = this.event_set.shift();
            
            var _event = ch.pop();
            if (_event === null)
            {
                _new_event_set.push(ch);
                continue;
            }

            this.module_set[_event[0]].process_event(ch, _event);
            this.event_set.push(ch);
        }
        this.event_set = _new_event_set;
    }
}
