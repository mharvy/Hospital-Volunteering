using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsCVA
{
    public partial class Form1 : Form
    {
        
        public Form1()
        {
            InitializeComponent();
        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {
            
        }

        private void numericUpDown13_ValueChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Get the user filename and number of trials
            string filename = "";
            int trials = 0;
            int sample_size = 0;
            try
            {
                filename = filenameBox.Text;
                trials = Convert.ToInt16(trialsBox.Text);
                sample_size = Convert.ToInt16(sampleSizeBox.Text);
            }
            catch { MessageBox.Show("Error Message"); }  // Error func will go here

            // This chunk gets the variables from the form, as two lists: one of all the first variables, and the 
            // next as all the second variables. It also checks to make sure they are the same length.
            // The two lists are var1DecList and var2DecList
            List<string> curvars1 = new List<string>();
            List<string> curvars2 = new List<string>();
            curvars1.Add(textBox1.Text);
            curvars1.Add(textBox2.Text);
            curvars1.Add(textBox3.Text);
            curvars1.Add(textBox4.Text);
            curvars1.Add(textBox5.Text);
            curvars1.Add(textBox6.Text);
            curvars1.Add(textBox7.Text);
            curvars1.Add(textBox8.Text);
            curvars1.Add(textBox9.Text);
            curvars1.Add(textBox10.Text);
            curvars2.Add(textBox11.Text);
            curvars2.Add(textBox12.Text);
            curvars2.Add(textBox13.Text);
            curvars2.Add(textBox14.Text);
            curvars2.Add(textBox15.Text);
            curvars2.Add(textBox16.Text);
            curvars2.Add(textBox17.Text);
            curvars2.Add(textBox18.Text);
            curvars2.Add(textBox19.Text);
            curvars2.Add(textBox20.Text);
            List<double> var1DecList= new List<double>();
            List<double> var2DecList = new List<double>();
            for (int i = 0; i < 10; i++)
            {
                if (curvars1[i] == "" && curvars2[i] == "") { continue; }
                else if (curvars1[i] == "" || curvars2[i] == "")
                {
                    MessageBox.Show("Error with input. Try again!");  // This will be replaced with an error func
                }
                else
                {
                    try
                    {
                        var1DecList.Add(Convert.ToDouble(curvars1[i]));
                        var2DecList.Add(Convert.ToDouble(curvars2[i]));
                    }
                    catch
                    {
                        MessageBox.Show("Error with input. Try again!");  // This will be replaced with an error func
                    }
                }
            }

            // This next chunk will get percentage data from form as a list of decimals, with max length being 13
            List<double> percentages1 = new List<double>();
            List<double> actualPercentages1 = new List<double>();
            percentages1.Add(Convert.ToDouble(numericUpDown1.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown2.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown3.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown4.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown5.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown6.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown7.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown8.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown9.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown10.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown11.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown12.Value));
            percentages1.Add(Convert.ToDouble(numericUpDown13.Value));
            for (int i = 0; i < 13; i++)
            {
                if (percentages1[i] == 0)
                {
                    continue;
                }
                else
                {
                    actualPercentages1.Add(percentages1[i] / (double)100);
                }
            }
            calculator jim = new calculator();
            for (int cur_vars_index = 0; cur_vars_index < var1DecList.Count; cur_vars_index++)
            {
                double var1 = var1DecList[cur_vars_index];
                double var2 = var2DecList[cur_vars_index];
                string cur_file = filename + "-" +var1.ToString() + "-" + var2.ToString() + ".csv";
                double answer = jim.Calculate(cur_file, trials, sample_size, var1, var2, actualPercentages1);
            }
            MessageBox.Show("Calculated. Check folder: " + System.IO.Path.GetDirectoryName(Application.ExecutablePath));
        }

        private void textBox21_TextChanged(object sender, EventArgs e)
        {

        }

        private void filenameBox_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void textBox21_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void splitContainer1_Panel2_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
