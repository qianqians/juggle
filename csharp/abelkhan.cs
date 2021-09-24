using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;

namespace abelkhan
{
    public class Exception : System.Exception
    {
        public Exception(string _err) : base(_err)
        {
        }
    }

    public interface Ichannel
    {
        void disconnect();
        void push(JArray ev);
    }

    public class Icaller
    {
        public Icaller(String _module_name, Ichannel _ch)
        {
            module_name = _module_name;
            ch = _ch;
        }

        public void call_module_method(String methodname, JArray argvs)
        {
			JArray _event = new JArray();
            _event.Add(module_name);
            _event.Add(methodname);
            _event.Add(argvs);

            try
            {
                ch.push(_event);
            }
            catch (System.Exception)
            {
                throw new abelkhan.Exception("error argvs");
            }
        }

        protected String module_name;
        private Ichannel ch;
    }

    public class Response : Icaller{
        public Response(String _module_name, Ichannel _ch) : base(_module_name, _ch){ 
        }
    }

    public class Imodule
    {
        public delegate void on_event(JArray _event);
        protected Dictionary<string, on_event> events;

        public Imodule(String _module_name){
            module_name = _module_name;
            events = new Dictionary<string, on_event>();
            current_ch = null;
            rsp = null;
        }

        public void reg_method(String method_name, on_event method){
            events.Add(method_name, method);
        }

        public void process_event(Ichannel _ch, JArray _event)
		{
			current_ch = _ch;
            try
            {
                String func_name = (String)_event[1];

                if (events.TryGetValue(func_name, out on_event method))
                {
                    try
                    {
                        method((JArray)_event[2]);
                    }
                    catch (System.Exception e)
                    {
                        throw new abelkhan.Exception(string.Format("function name:{0} System.Exception:{1}", func_name, e));
                    }
                }
                else
                {
                    throw new abelkhan.Exception(string.Format("do not have a function named::{0}", func_name));
                }
            }
            catch (System.Exception e)
            {
                throw new abelkhan.Exception(string.Format("System.Exception:{0}", e));
            }
            finally
            {
                current_ch = null;
            }
        }

		public Ichannel current_ch;
        public Response rsp;
		public String module_name;
    }

    public class modulemng
    {
		public modulemng()
		{
			module_set = new Dictionary<string, Imodule>();
		}

		public void reg_module(Imodule module)
        {
			module_set.Add(module.module_name, module);
        }

		public void unreg_module(Imodule module)
        {
			module_set.Remove(module.module_name);
        }

        public void process_event(Ichannel _ch, JArray _event){
            try{
                String module_name = (String)_event[0];
                if (module_set.TryGetValue(module_name, out Imodule _module))
                {
                    _module.process_event(_ch, _event);
                }
                else
                {
                    throw new abelkhan.AbelkhanException(string.Format("do not have a module named::{0}", module_name));
                }
            }
            catch (System.Exception e)
            {
                throw new abelkhan.Exception(string.Format("System.Exception:{0}", e));
            }
        }

        private Dictionary<string, Imodule> module_set;
    }
}