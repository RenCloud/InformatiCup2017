namespace RepoTagGui
{
    partial class Form1
    {
        /// <summary>
        /// Erforderliche Designervariable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Verwendete Ressourcen bereinigen.
        /// </summary>
        /// <param name="disposing">True, wenn verwaltete Ressourcen gelöscht werden sollen; andernfalls False.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Vom Windows Form-Designer generierter Code

        /// <summary>
        /// Erforderliche Methode für die Designerunterstützung.
        /// Der Inhalt der Methode darf nicht mit dem Code-Editor geändert werden.
        /// </summary>
        private void InitializeComponent()
        {
            this.b_createTCPConnection = new System.Windows.Forms.Button();
            this.tb_ip = new System.Windows.Forms.TextBox();
            this.tb_port = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.l_response = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // b_createTCPConnection
            // 
            this.b_createTCPConnection.Location = new System.Drawing.Point(272, 50);
            this.b_createTCPConnection.Name = "b_createTCPConnection";
            this.b_createTCPConnection.Size = new System.Drawing.Size(264, 23);
            this.b_createTCPConnection.TabIndex = 0;
            this.b_createTCPConnection.Text = "Create TCP Connection";
            this.b_createTCPConnection.UseVisualStyleBackColor = true;
            this.b_createTCPConnection.Click += new System.EventHandler(this.b_createTCPConnection_Click);
            // 
            // tb_ip
            // 
            this.tb_ip.Location = new System.Drawing.Point(272, 24);
            this.tb_ip.Name = "tb_ip";
            this.tb_ip.Size = new System.Drawing.Size(100, 20);
            this.tb_ip.TabIndex = 1;
            this.tb_ip.Text = "IP";
            // 
            // tb_port
            // 
            this.tb_port.Location = new System.Drawing.Point(436, 24);
            this.tb_port.Name = "tb_port";
            this.tb_port.Size = new System.Drawing.Size(100, 20);
            this.tb_port.TabIndex = 2;
            this.tb_port.Text = "PORT";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(272, 137);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(55, 13);
            this.label1.TabIndex = 3;
            this.label1.Text = "Response";
            // 
            // l_response
            // 
            this.l_response.AutoSize = true;
            this.l_response.Location = new System.Drawing.Point(336, 137);
            this.l_response.Name = "l_response";
            this.l_response.Size = new System.Drawing.Size(35, 13);
            this.l_response.TabIndex = 4;
            this.l_response.Text = "label2";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(932, 515);
            this.Controls.Add(this.l_response);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.tb_port);
            this.Controls.Add(this.tb_ip);
            this.Controls.Add(this.b_createTCPConnection);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button b_createTCPConnection;
        private System.Windows.Forms.TextBox tb_ip;
        private System.Windows.Forms.TextBox tb_port;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label l_response;
    }
}

