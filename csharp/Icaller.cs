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
                var _tmplenght = _tmpdata.Length + 4;

                byte[] buf = new byte[4 + _tmplenght];
                buf[0] = (byte)(_tmplenght & 0xff);
                buf[1] = (byte)((_tmplenght >> 8) & 0xff);
                buf[2] = (byte)((_tmplenght >> 16) & 0xff);
                buf[3] = (byte)((_tmplenght >> 24) & 0xff);
                _tmpdata.CopyTo(buf, 4);

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
