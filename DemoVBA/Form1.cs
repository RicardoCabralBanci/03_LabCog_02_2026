using System;
using System.Drawing;
using System.Windows.Forms;

namespace DemoVBA
{
    // TELA 1: O MENU PRINCIPAL
    public partial class Form1 : Form
    {
        private GroupBox gbOpcoes;
        private RadioButton rbCCMX;
        private RadioButton rbPLT;
        private RadioButton rbPCK;
        private Button btnAvancar;

        public Form1()
        {
            this.Text = "Sistema Principal";
            this.Size = new Size(350, 300);
            this.StartPosition = FormStartPosition.CenterScreen;

            // 1. Criando o Grupo (Frame)
            gbOpcoes = new GroupBox();
            gbOpcoes.Text = "Selecione o Módulo:";
            gbOpcoes.Location = new Point(30, 20);
            gbOpcoes.Size = new Size(250, 150);
            this.Controls.Add(gbOpcoes);

            // 2. Criando as Opções (OptionButtons)
            // Adicionamos elas DENTRO do gbOpcoes, não do Form
            rbCCMX = CriarOpcao("CCMX - Controle", 30);
            rbPLT  = CriarOpcao("PLT - Paletização", 60);
            rbPCK  = CriarOpcao("PCK - Packing", 90);
            
            // Seleciona o primeiro por padrão
            rbCCMX.Checked = true; 

            // 3. Botão para Abrir (CommandButton)
            btnAvancar = new Button();
            btnAvancar.Text = "Abrir Módulo >>";
            btnAvancar.Location = new Point(30, 190);
            btnAvancar.Size = new Size(250, 40);
            btnAvancar.Click += new EventHandler(BtnAvancar_Click); // O Evento
            this.Controls.Add(btnAvancar);
        }

        // Função auxiliar para não repetir código (Boas práticas de C#)
        private RadioButton CriarOpcao(string texto, int y)
        {
            RadioButton rb = new RadioButton();
            rb.Text = texto;
            rb.Location = new Point(20, y);
            rb.AutoSize = true;
            gbOpcoes.Controls.Add(rb); // Adiciona ao Frame
            return rb;
        }

        private void BtnAvancar_Click(object sender, EventArgs e)
        {
            // Descobre qual foi selecionado
            string escolha = "";
            if (rbCCMX.Checked) escolha = "CCMX";
            else if (rbPLT.Checked) escolha = "PLT";
            else if (rbPCK.Checked) escolha = "PCK";

            // ABRE A OUTRA TELA PASSANDO A ESCOLHA
            // Isso equivale a criar um novo UserForm e passar dados
            DetalheForm novaTela = new DetalheForm(escolha);
            
            this.Hide(); // Esconde o menu principal
            novaTela.ShowDialog(); // Abre a nova tela e espera fechar
            this.Show(); // Mostra o menu de volta quando a outra fechar
        }
    }

    // TELA 2: A TELA DE DETALHES (SECUNDÁRIA)
    public class DetalheForm : Form
    {
        public DetalheForm(string moduloSelecionado)
        {
            this.Text = "Módulo: " + moduloSelecionado;
            this.Size = new Size(400, 200);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.WhiteSmoke; // Só para diferenciar

            // Título
            Label lblTitulo = new Label();
            lblTitulo.Text = "Bem-vindo ao " + moduloSelecionado;
            lblTitulo.Font = new Font("Arial", 16, FontStyle.Bold);
            lblTitulo.AutoSize = true;
            lblTitulo.Location = new Point(20, 20);
            lblTitulo.ForeColor = Color.DarkBlue;
            this.Controls.Add(lblTitulo);

            // Descrição
            Label lblDesc = new Label();
            lblDesc.Text = "Aqui iriam os controles específicos do " + moduloSelecionado + ".\n" +
                           "Botões, Grids e Inputs deste processo.";
            lblDesc.Location = new Point(25, 60);
            lblDesc.AutoSize = true;
            this.Controls.Add(lblDesc);

            // Botão Fechar
            Button btnFechar = new Button();
            btnFechar.Text = "Voltar";
            btnFechar.Location = new Point(250, 100);
            btnFechar.Click += (s, e) => this.Close(); // Atalho moderno (Lambda) para fechar
            this.Controls.Add(btnFechar);
        }
    }
}
