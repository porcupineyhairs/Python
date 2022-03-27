import datetime

from SqlHelper import MsSqlHelper
import pandas as pd
import numpy as np
import time


class ErpBom:
	def __init__(self, mssql):
		self.mssql = mssql
		if not isinstance(self.mssql, MsSqlHelper):
			raise self.__ErpException('__init__ 传入参数mssql应为MsSqlHelper实例，请检查传入参数')
		
	def __del__(self):
		pass

	def bom_up(self, ph):
		bom_up = self.__BomUp(self.mssql, self.__ErpException)
		rtn_df = bom_up.work(ph)
		del bom_up
		return rtn_df
	
	def bom_down(self, ph):
		bom_down = self.__BomDown(self.mssql, self.__ErpException)
		rtn_df = bom_down.work(ph)
		del bom_down
		return rtn_df
	
	def bom_down_pz(self, ph, pz='', rq='', clean=False):
		bomdown_pz = self.__BomDown_Pz(self.mssql, self.__ErpException)
		rtn_df = bomdown_pz.work(ph, pz, rq, clean)
		del bomdown_pz
		return rtn_df
	
	def wlno_pz(self, ph, pz=None):
		wlno_pz = self.__WlnoPz(self.mssql, self.__ErpException)
		rtn_df = wlno_pz.work(ph, pz)
		del wlno_pz
		return rtn_df
	
	class __BaseClass:
		def __init__(self, mssql, exception):
			self.mssql = mssql
			self.exception = exception
			self.rtn_df = pd.DataFrame(columns=['材料品号', '品号属性', '成品品号', '成品品名', '成品规格'])
			if self.mssql is None:
				raise exception('mssql is None')
		
		def __del__(self):
			del self.rtn_df
	
		def __check_input(self, ph):
			if not (isinstance(ph, list) or isinstance(ph, str) or isinstance(ph, pd.DataFrame)):
				raise self.exception('传入参数ph应为list或str或pd.df，请检查传入参数')
			
	class __BomUp:
		def __init__(self, mssql, exception):
			self.mssql = mssql
			self.exception = exception
			self.rtn_df = pd.DataFrame(columns=['材料品号', '品号属性', '品号', '品名', '规格'])
			if self.mssql is None:
				raise exception('mssql is None')
		
		def __del__(self):
			del self.rtn_df
			
		def work(self, ph):
			if not (isinstance(ph, list) or isinstance(ph, str) or isinstance(ph, pd.DataFrame)):
				raise self.exception('传入参数ph应为list或str或pd.df，请检查传入参数')
			if isinstance(ph, pd.DataFrame):
				col_list = ph.columns.tolist()
				if '品号' in col_list:
					for row in range(len(ph)):
						if not self.__cp_select(ph.at[row, '品号']):
							self.__select(ph.at[row, '品号'])
				else:
					raise self.exception('传入pd.df不存在列名 品号 ，请检查传入参数')
			if isinstance(ph, list):
				for ph_tmp in ph:
					if not self.__cp_select(ph_tmp):
						self.__select(ph_tmp)
			if isinstance(ph, str):
				if not self.__cp_select(ph):
					self.__select(ph)
				
			return self.rtn_df
		
		def __cp_select(self, pinhao, pinhao2=None):
			if pinhao2 is None:
				pinhao2 = pinhao
			
			sql_str = r"SELECT '{1}' 材料品号, RTRIM(MB025) 品号属性, RTRIM(MB001) 品号, RTRIM(MB002) 品名, RTRIM(MB003) 规格  " \
			         r"FROM INVMB WHERE MB025='M' AND MB109='Y' AND MB001 = '{0}' "
			df = self.mssql.sqlWork(sqlStr=sql_str.format(pinhao2, pinhao))
			if df is not None:
				self.rtn_df = self.rtn_df.append(df.loc[0], ignore_index=True)
				return True
			else:
				return False
		
		def __select(self, pinhao, pinhao2=None):
			if pinhao2 is None:
				pinhao2 = pinhao
			
			sql_str = r"SELECT '{1}' 材料品号, RTRIM(MB025) 品号属性, RTRIM(CB001) 品号, RTRIM(MB002) 品名, RTRIM(MB003) 规格 " \
			         r"FROM BOMCB INNER JOIN INVMB ON MB001 = CB001 AND MB109 = 'Y' " \
			         r"WHERE (ISNULL(RTRIM(CB014), '') = '' OR CB014 >= CONVERT(VARCHAR(8), GETDATE(), 112)) AND CB005 = '{0}' " \
			         r"ORDER BY CB001 "
			
			df = self.mssql.sqlWork(sqlStr=sql_str.format(pinhao2, pinhao))
			if df is not None:
				for row in range(len(df)):
					shuxing = df.at[row, '品号属性']
					shangjie = df.at[row, '品号']
					
					if shuxing == 'M':
						self.rtn_df = self.rtn_df.append(df.loc[row], ignore_index=True)
					else:
						self.__select(pinhao, shangjie)
						
	class __BomDown:
		def __init__(self, mssql, exception):
			self.mssql = mssql
			self.exception = exception
			self.rtn_df = pd.DataFrame(columns=['层级', '品号', '品名', '规格', 'BOM序号', '品号属性', '工艺编号', '生效日期',
			                                    '失效日期', '供应商名称', '默认选择'])
			if self.mssql is None:
				raise exception('mssql is None')
		
		def __del__(self):
			del self.rtn_df
		
		def work(self, ph):
			if not (isinstance(ph, list) or isinstance(ph, str) or isinstance(ph, pd.DataFrame)):
				raise self.exception('传入参数ph应为list或str或pd.df，请检查传入参数')
			if isinstance(ph, pd.DataFrame):
				col_list = ph.columns.tolist()
				if '品号' in col_list:
					for row in range(len(ph)):
						self.__select(ph.at[row, '品号'])
				else:
					raise self.exception('传入pd.df不存在列名 品号 ，请检查传入参数')
			if isinstance(ph, list):
				for ph_tmp in ph:
					self.__select(ph_tmp)
			if isinstance(ph, str):
				self.__select(ph)
			
			return self.rtn_df
		
		def __select(self, pinhao, level=0):
			if level == 0:
				sql_str = r"SELECT {1} 层级, RTRIM(MB001) 品号, RTRIM(MB002) 品名, RTRIM(MB003) 规格, RTRIM(MB025) 品号属性 " \
				          r"FROM INVMB WHERE RTRIM(MB001) = '{0}' "
				df = self.mssql.sqlWork(sql_str.format(pinhao, level))
				if df is not None:
					level += 1
					self.rtn_df = self.rtn_df.append(df.loc[0], ignore_index=True)
					self.__wl_select(pinhao, level)
		
		def __wl_select(self, pinhao, level):
			sql_str = (r"SELECT DISTINCT {1} 层级, "
			           r"RTRIM(CB005) 品号, "
			           r"RTRIM(MB002) 品名, "
			           r"RTRIM(MB003) 规格, "
			           r"RTRIM(CB004) BOM序号, "
			           r"RTRIM(INVMB.MB025) 品号属性, "
			           r"RTRIM(MW001) 工艺编号, "
			           r"(CASE WHEN RTRIM(CB013) IS NULL THEN '' WHEN RTRIM(CB013) = '' THEN '' "
			           r"ELSE SUBSTRING(RTRIM(CB013),1,4) + '-' + SUBSTRING(RTRIM(CB013),5,2) + '-' + "
			           r"SUBSTRING(RTRIM(CB013),7,2) END ) 生效日期, "
			           r"(CASE WHEN RTRIM(CB014) IS NULL THEN '' WHEN RTRIM(CB014) = '' THEN '' "
			           r"ELSE SUBSTRING(RTRIM(CB014),1,4) + '-' + SUBSTRING(RTRIM(CB014),5,2) + '-' + "
			           r"SUBSTRING(RTRIM(CB014),7,2) END ) 失效日期, "
			           r"RTRIM(PURMA.MA002) 供应商名称, "
			           r"RTRIM(CB015) 默认选择 "
			           r"FROM BOMCB "
			           r"LEFT JOIN CMSMW ON MW001 = CB011 "
			           r"LEFT JOIN INVMB ON CB005 = INVMB.MB001 "
			           r"LEFT JOIN BOMCA ON CA003 = CB005 "
			           r"LEFT JOIN INVMA ON INVMA.MA002 = INVMB.MB005 "
			           r"LEFT JOIN PURMA ON PURMA.MA001 = INVMB.MB032 "
			           r"WHERE CB001 = '{0}' ORDER BY RTRIM(CB004) ")
			
			df = self.mssql.sqlWork(sqlStr=sql_str.format(pinhao, level))
			if df is not None:
				for row in range(len(df)):
					pinhao2 = df.at[row, '品号']
					shuxing = df.at[row, '品号属性']
					
					shuxing_lib = {'P': '采购件', 'S': '委外件', 'C': '配置件', 'Y': '虚设件', 'M': '自制件'}
					shuxing2 = shuxing_lib[str(shuxing)]
					
					self.rtn_df = self.rtn_df.append(df.loc[row], ignore_index=True)
					
					if shuxing != 'P':
						self.__wl_select(pinhao2, level + 1)
						
	class __BomDown_Pz:
		def __init__(self, mssql, exception):
			self.mssql = mssql
			self.exception = exception
			self.rtn_df = None
			if self.mssql is None:
				raise exception('mssql is None')
		
		def __del__(self):
			del self.rtn_df
		
		def work(self, ph, pz, rq, clean):
			if not (isinstance(ph, int) or isinstance(ph, str)):
				raise self.exception('传入参数ph应为str，请检查传入参数')
			if isinstance(ph, pd.DataFrame):
				col_list = ph.columns.tolist()
				if '品号' in col_list and '客户配置' in col_list:
					for row in range(len(ph)):
						self.__select(ph.at[row, '品号'], ph.at[row, '客户配置'], rq)
				else:
					raise self.exception('传入pd.df不存在列名 品号,客户配置 ，请检查传入参数')
			if isinstance(ph, str) or isinstance(ph, int):
				self.__select(ph, pz, rq)
			
			if clean and self.rtn_df is not None:
				self.__clean()
				
			return self.rtn_df.reset_index(drop=True)
		
		def __select(self, ph, pz='', rq=''):
			sql_str = r"select * from [dbo].[f_bom_extend_fliter_with_pz]('{0}', '{2}', '{1}') " \
			          r"order by sid, len(sid)"
			
			if rq == '':
				rq = datetime.datetime.now().strftime("yyyyMMdd")
			
			df = self.mssql.sqlWork(sql_str.format(ph, pz, rq))
			if self.rtn_df is None:
				self.rtn_df = df
			else:
				self.rtn_df = self.rtn_df.append(df, ignore_index=True)
		
		def __clean(self):
			max_lv = np.nanmax(self.rtn_df[['lv']].values)
			# print(max_lv)
			for lv_tmp in range(max_lv + 1):
				# 查出配置件的层级
				df_tmp1 = self.rtn_df.loc[(self.rtn_df['lv'] == lv_tmp) & (self.rtn_df['MB025'] == 'C'),
				                          ['lv', 'TR017N', 'MD001', 'MD003', 'MD00300', 'sid']]
				if len(df_tmp1) > 0:
					df_tmp1 = df_tmp1.reset_index(drop=True)
					for row_tmp1 in range(len(df_tmp1)):
						# 查出配置件下非选中项
						sid = df_tmp1.at[row_tmp1, 'sid']
						MD003 = df_tmp1.at[row_tmp1, 'MD003']
						df_tmp2 = self.rtn_df.loc[(self.rtn_df['lv'] == lv_tmp + 1) & (self.rtn_df['TR017N'] == 'N')
						                          & (self.rtn_df['MD00300'] == MD003) & (self.rtn_df['sid'].str.startswith(sid)),
				                                  ['lv', 'TR017N', 'MD001', 'MD003', 'MD00300', 'sid']]
						df_tmp2 = df_tmp2.reset_index(drop=True)
						# print(df_tmp2)
						for row_tmp2 in range(len(df_tmp2)):
							# 删除非选择项及其下阶
							sid2 = df_tmp2.at[row_tmp2, 'sid']
							df_tmp3 = self.rtn_df.loc[(self.rtn_df['sid'].str.startswith(sid2)),
				                                  ['lv', 'TR017N', 'MD001', 'MD003', 'MD00300', 'sid']]
							# print(df_tmp3)
							self.rtn_df = self.rtn_df.drop(index=df_tmp3.index)
						
	class __WlnoPz:
		def __init__(self, mssql, exception):
			self.mssql = mssql
			self.exception = exception
			self.rtn_df = None
			if self.mssql is None:
				raise exception('mssql is None')
		
		def __del__(self):
			del self.rtn_df
		
		def work(self, ph, pz=None):
			if not (isinstance(ph, list) or isinstance(ph, str) or isinstance(ph, pd.DataFrame)):
				raise self.exception('传入参数ph应为list或str或pd.df，请检查传入参数')
			if isinstance(ph, pd.DataFrame):
				col_list = ph.columns.tolist()
				if '品号' in col_list:
					if '客户配置' in col_list:
						for row in range(len(ph)):
							self.__select(ph.at[row, '品号'], ph.at[row, '客户配置'])
					else:
						for row in range(len(ph)):
							self.__select(ph.at[row, '品号'])
				else:
					raise self.exception('传入pd.df不存在列名 品号 ，请检查传入参数')
			if isinstance(ph, list):
				for ph_tmp in ph:
					self.__select(ph_tmp)
			if isinstance(ph, str):
				self.__select(ph, pz)
			
			return self.rtn_df
		
		def __select(self, ph, pz=None):
			sql_str = r"SELECT RTRIM(TQ001) 品号, RTRIM(INVMB.MB002) 品名, RTRIM(INVMB.MB003) 规格, " \
			          r"RTRIM(ISNULL(TQ002, '')) 客户配置, " \
			          r"ISNULL(MIN(TC003), '') 最早使用日期, ISNULL(MAX(TC003), '') 最后使用日期 " \
			          r"FROM COPTQ " \
			          r"LEFT JOIN COPTD ON TD004 = TQ001 AND TD053 = TQ002 " \
			          r"LEFT JOIN COPTC ON TC001 = TD001 AND TC002 = TC002 AND TC027 = 'Y' AND TD008 != 0 " \
			          r"INNER JOIN INVMB ON MB001 = TQ001 AND MB025 = 'M' " \
			          r"WHERE TQ006 = 'Y' " \
			          r"AND TD004 = '{0}'"
			if pz is not None:
				sql_str += r"AND TD053 = '{0}' ".format(pz)
				
			sql_str += r"GROUP BY TQ001, MB002, MB003, TQ002 " \
			           r"ORDER BY TQ001, TQ002 "
			df = self.mssql.sqlWork(sql_str.format(ph))
			if self.rtn_df is None:
				self.rtn_df = df
			else:
				self.rtn_df = self.rtn_df.append(df, ignore_index=True)
			
	class __ErpException(Exception):
		def __init__(self, err_inf):
			self.err_inf = err_inf
			super().__init__(self)
		
		def __str__(self):
			return self.err_inf
