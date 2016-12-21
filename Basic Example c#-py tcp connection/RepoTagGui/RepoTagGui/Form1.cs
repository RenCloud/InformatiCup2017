using System;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.Serialization.Formatters.Binary;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Windows.Forms;

namespace RepoTagGui {
    public partial class Form1 : Form {
        private NetworkStream inOUt;
        private TcpClient tcpClient;

        public Form1() {
            InitializeComponent();
        }

        private void b_createTCPConnection_Click(object sender, EventArgs e) {
            b_createTCPConnection.Enabled =false ;
            tcpClient = new TcpClient(tb_ip.Text, int.Parse(tb_port.Text));
            inOUt = tcpClient.GetStream();
            var sendBytes = Encoding.ASCII.GetBytes("TestString");
            inOUt.Write(sendBytes, 0, sendBytes.Length);
            Console.WriteLine("Send Message: {0}", Encoding.ASCII.GetString(sendBytes, 0, sendBytes.Length));
            while (!l_response.Text.Equals("End")) {
                sendBytes = new byte[1024];
                var bytes = inOUt.Read(sendBytes, 0, sendBytes.Length);
                var responseData = System.Text.Encoding.ASCII.GetString(sendBytes, 0, bytes);
                l_response.Text = responseData;
                Refresh();
                Application.DoEvents();         
            }

            inOUt.Close();
            tcpClient.Close();

            b_createTCPConnection.Enabled =true ;
        }
    }
}



    