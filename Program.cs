using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace WindowsCVA
{
    public class calculator
    {
        public calculator()
        {
        }

        public Random r = new Random();

        public List<double> Modelmaker(double var1, double var2, double percent, int sample_size)
        {
            List<double> model = new List<double>();

            for (int cur_data_index = 0; cur_data_index < sample_size; cur_data_index++)
            {
                double curcutoff = r.NextDouble();
                if (curcutoff < percent) { model.Add(var1); }
                else { model.Add(var2); }
            }
            return model;
        }

        public double Calculate(string filename, int trials, int sample_size, double var1, double var2, List<double> percentages)
        {
            List<List<double>> cur_sums_list_list = new List<List<double>>();
            foreach (double percent in percentages)
            {
                List<double> cur_sums_list = new List<double>();
                for (int trial = 0; trial < trials; trial++)
                {
                    List<double> cur_model = Modelmaker(var1, var2, percent, sample_size);
                    double cur_sum = cur_model.Sum();
                    cur_sums_list.Add(cur_sum);
                }
                cur_sums_list_list.Add(cur_sums_list);
            }

            using (StreamWriter sw = new StreamWriter(filename))
            {
                // Get heading for CSV file and write
                string heading = " ,";
                foreach (double percent in percentages)
                {
                    heading += ((percent * 100).ToString() + ",");
                }
                heading = heading.TrimEnd(',');
                sw.WriteLine(heading);

                for (int trial = 0; trial < trials; trial++)
                {
                    string cur_row = trial.ToString() + ",";
                    for (int percent_index = 0; percent_index < percentages.Count; percent_index++)
                    {
                        cur_row += (cur_sums_list_list[percent_index][trial].ToString() + ",");
                    }
                    cur_row = cur_row.TrimEnd(',');
                    sw.WriteLine(cur_row);

                }
                // All the precious data analysis
                List<double> all_stnds = new List<double>();
                List<double> all_means = new List<double>();
                List<double> all_cvs = new List<double>();
                List<double> all_xp2s = new List<double>();
                // All the row strings
                string means_row = "Mean,";
                string stnds_row = "Standard Deviation,";
                string cvs_row = "% CV,";
                string xp2s_row = "x + 2s,";
                for (int percent_index = 0; percent_index < percentages.Count; percent_index++)
                {
                    // Get the mean
                    double cur_mean = cur_sums_list_list[percent_index].Average();
                    all_means.Add(cur_mean);
                    means_row += (cur_mean.ToString() + ",");
                    // Get the standard deviation
                    double numerator = cur_sums_list_list[percent_index].Sum(d => Math.Pow(d - cur_mean, 2));
                    double cur_stnd = Math.Sqrt((numerator) / (trials)); // This line may be wrong, check later
                    all_stnds.Add(cur_stnd);
                    stnds_row += (cur_stnd.ToString() + ",");
                    // Get the coefficient of variation
                    double cur_cv = cur_stnd / cur_mean * 100;
                    all_cvs.Add(cur_cv);
                    cvs_row += (cur_cv.ToString() + ",");
                    // Get 'x + 2s'
                    double cur_xp2s = cur_mean + (2 * cur_stnd);
                    all_xp2s.Add(cur_xp2s);
                    xp2s_row += (cur_xp2s.ToString() + ",");
                }
                // Format row strings correctly and finally write
                means_row = means_row.TrimEnd(',');
                sw.WriteLine(means_row);

                stnds_row = stnds_row.TrimEnd(',');
                sw.WriteLine(stnds_row);

                cvs_row = cvs_row.TrimEnd(',');
                sw.WriteLine(cvs_row);

                xp2s_row = xp2s_row.TrimEnd(',');
                sw.WriteLine(xp2s_row);
            }
            return 1;
        }
    }


    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}
