import { apiClient } from '../../../shared/api/client';
import type { CursusListItem, CursusDetail } from '../model/types';

export const cursusApi = {
  async getList(): Promise<CursusListItem[]> {
    return apiClient<CursusListItem[]>('/api/v1/cursus');
  },

  async getById(id: string): Promise<CursusDetail> {
    return apiClient<CursusDetail>(`/api/v1/cursus/${id}`);
  },
};
