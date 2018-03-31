function process(){
    this.module_set = {};
    
    this.event_set = new Array();
    this.add_event = new Array();
    this.remove_event = new Array();

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
        this.add_event = new Array();

        var _new_event_set = new Array();
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
        this.remove_event = new Array();

        for(ch in this.event_set)
        {
			while (true)
			{
                var _event = this.event_set[ch].pop();
                if (_event === null)
                {
                    break;
                }
                this.module_set[_event[0]].process_event(this.event_set[ch], _event);
            }
        }
    }
}
