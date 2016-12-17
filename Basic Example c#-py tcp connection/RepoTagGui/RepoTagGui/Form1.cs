using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Windows.Forms;

namespace RepoTagGui {
    public partial class Form1 : Form {
        private Stream inOUt;
        private TcpClient tcpClient;

        public Form1() {
            InitializeComponent();
        }

        private void b_createTCPConnection_Click(object sender, EventArgs e) {
            b_createTCPConnection.Enabled =false ;
            tcpClient = new TcpClient(tb_ip.Text, int.Parse(tb_port.Text));
            inOUt = tcpClient.GetStream();
            var sendBytes = Encoding.ASCII.GetBytes("TestString to Start Training on Python Server really long...");
            inOUt.Write(sendBytes, 0, sendBytes.Length);
            tcpClient.Close();
            b_createTCPConnection.Enabled =true ;
        }
    }
}