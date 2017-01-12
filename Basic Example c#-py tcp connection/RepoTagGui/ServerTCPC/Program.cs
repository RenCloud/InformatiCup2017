using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace ServerTCPC
{
    class Program
    {
        
              private const int portNum = 13;

        public static int Main(string[] args)
        {
            var done = false;

            var listener = new TcpListener(IPAddress.Any,portNum);

            listener.Start();

            while (!done)
            {
                Console.Write("Waiting for connection...");
                var client = listener.AcceptTcpClient();

                Console.WriteLine("Connection accepted.");
                var ns = client.GetStream();
                
                var byteTime = Encoding.ASCII.GetBytes(DateTime.Now.ToString());

                try
                {
                    ns.Write(byteTime, 0, byteTime.Length);
                    ns.Close();
                    client.Close();
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.ToString());
                }
            }

            listener.Stop();

            return 0;
        }


    
    }
}
