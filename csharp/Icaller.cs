using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;

namespace juggle
{
    public class Icaller
    {
        public Icaller(Ichannel _ch)
        {
            ch = _ch;
        }

        public void call_module_method(String methodname, ArrayList argvs)
        {
			ArrayList _event = new ArrayList();
            _event.Add(module_name);
            _event.Add(methodname);
            _event.Add(argvs);

            try
            {
                var _tmp = Json.Jsonparser.pack(_event);
                var _tmpdata = System.Text.Encoding.UTF8.GetBytes(_tmp);

                byte[] buf = new byte[4 + _tmpdata.Length];
                buf[0] = (byte)(_tmpdata.Length & 0xff);
                buf[1] = (byte)((_tmpdata.Length >> 8) & 0xff);
                buf[2] = (byte)((_tmpdata.Length >> 16) & 0xff);
                buf[3] = (byte)((_tmpdata.Length >> 24) & 0xff);
                for(int i = 0; i < _tmpdata.Length; i++)
                {
                    buf[i+4] = (byte)_tmpdata[i];
                }

                ch.senddata(buf);
            }
            catch (Json.Exception)
            {
                throw new juggle.Exception("error argvs");
            }
        }

        protected String module_name;
        private Ichannel ch;
    }
}
